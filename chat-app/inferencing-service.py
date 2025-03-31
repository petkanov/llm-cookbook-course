import modal
from pathlib import Path

vllm_image = modal.Image.debian_slim(python_version="3.12").pip_install(
    "vllm==0.6.3post1", "fastapi[standard]==0.115.4"
)

MODELS_DIR = "/llm"
MODEL_REPO_ID = "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16" # quantized to 4-bit
MODEL_REVISION = "a7c09948d9a632c2c840722f519672cd94af885d"

try:
    volume = modal.Volume.lookup("llm", create_if_missing=False)
except modal.exception.NotFoundError:
    raise RuntimeError("Volume not found. Please deploy [download-model-service] first")

app = modal.App("vllm-chat")

N_GPU = 1  # first upgrade to more powerful GPUs, and only then increase GPU count
TOKEN = "my-token"  # auth token, for production use, replace with a modal.Secret

MINUTE = 60
HOUR = 60 * MINUTE


@app.function(
    image=vllm_image,
    gpu=modal.gpu.T4(count=N_GPU),
    container_idle_timeout=5 * MINUTE, # how long the container will wait for new requests before shutting down
    volumes={MODELS_DIR: volume},
    timeout=24 * HOUR, # how long the function will run before being terminated
    allow_concurrent_inputs=1000 # how many requests can be processed concurrently
)
@modal.asgi_app()
def serve():
    import fastapi, time
    from pathlib import Path
    import vllm.entrypoints.openai.api_server as api_server
    from vllm.engine.arg_utils import AsyncEngineArgs
    from vllm.engine.async_llm_engine import AsyncLLMEngine
    from vllm.entrypoints.logger import RequestLogger
    from vllm.entrypoints.openai.serving_chat import OpenAIServingChat
    from vllm.entrypoints.openai.serving_completion import OpenAIServingCompletion
    from vllm.entrypoints.openai.serving_engine import BaseModelPath
    from vllm.usage.usage_lib import UsageContext

    volume.reload() 

    model_path = Path(MODELS_DIR) / MODEL_REPO_ID
    if not model_path.exists() or not any(model_path.glob("*")): 
        print(f"Model not found at {model_path}, downloading...")

        download_model_function = modal.Function.from_name("download-model-service", "download_model")
        download_model_function.remote(MODEL_REPO_ID, MODEL_REVISION)

        while not is_model_downloaded(model_path):
            print(f"Model not downloaded yet, waiting...")
            time.sleep(5)
            volume.reload() 

        print(f"Model downloaded to {model_path}")
    else:
        print(f"Model already exists at {model_path}")


    web_app = fastapi.FastAPI(
        title=f"OpenAI-compatible {MODEL_REPO_ID} server",
        description="Run an OpenAI-compatible LLM server with vLLM on modal.com 🚀",
        version="0.0.1",
        docs_url="/docs",
    )

    http_bearer = fastapi.security.HTTPBearer(
        scheme_name="Bearer Token",
        description="See code for authentication details.",
    )
    web_app.add_middleware(
        fastapi.middleware.cors.CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    async def is_authenticated(api_key: str = fastapi.Security(http_bearer)):
        if api_key.credentials != TOKEN:
            raise fastapi.HTTPException(
                status_code=fastapi.status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authentication credentials",
            )
        return {"username": "authenticated_user"}

    router = fastapi.APIRouter(dependencies=[fastapi.Depends(is_authenticated)])

    router.include_router(api_server.router)
    web_app.include_router(router)

    engine_args = AsyncEngineArgs(
        model=MODELS_DIR + "/" + MODEL_REPO_ID,
        tensor_parallel_size=N_GPU, # allows model computations to be distributed across multiple GPUs for better performance
        gpu_memory_utilization=0.90, #  allowing the engine to use up to 90% of available GPU memory to balance between performance and resource allocation
        max_model_len=8096, # maximum number of tokens the model can process in a single request
        enforce_eager=False, 
    )

    engine = AsyncLLMEngine.from_engine_args(
        engine_args, usage_context=UsageContext.OPENAI_API_SERVER
    )

    model_config = get_model_config(engine)

    request_logger = RequestLogger(max_log_len=2048)

    base_model_paths = [
        BaseModelPath(name=MODEL_REPO_ID.split("/")[1], model_path=MODEL_REPO_ID)
    ]

    api_server.chat = lambda s: OpenAIServingChat(
        engine,
        model_config=model_config,
        base_model_paths=base_model_paths,
        chat_template=None,
        response_role="assistant",
        lora_modules=[],
        prompt_adapters=[],
        request_logger=request_logger,
    )
    api_server.completion = lambda s: OpenAIServingCompletion(
        engine,
        model_config=model_config,
        base_model_paths=base_model_paths,
        lora_modules=[],
        prompt_adapters=[],
        request_logger=request_logger,
    )

    return web_app

# The function call aims to obtain the model's configuration from the engine. 
# This configuration may include parameters like the model's architecture, 
# input/output size, supported features, or other meta-information about the model.
def get_model_config(engine):
    import asyncio

    try:
        event_loop = asyncio.get_running_loop()
    except RuntimeError:
        event_loop = None

    if event_loop is not None and event_loop.is_running():
        model_config = event_loop.run_until_complete(engine.get_model_config())
    else:
        model_config = asyncio.run(engine.get_model_config())

    return model_config

def is_model_downloaded(model_path: Path) -> bool:
    completion_file = model_path / "download_complete"
    return completion_file.exists()