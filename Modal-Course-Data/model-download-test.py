from pathlib import Path
from modal import App, Volume, Image

app = App("Volumes-test")

MODEL_DIR = Path("/models")

image = (
    Image.debian_slim()
    .pip_install("huggingface_hub[hf_transfer]","transformers","torch", "accelerate")  
    .env({"HF_HUB_ENABLE_HF_TRANSFER": "1"}) 
)
volume = Volume.from_name("testing-model-weights-directory", create_if_missing=True)

@app.function(
    volumes={MODEL_DIR: volume},  # "mount" the Volume, sharing it with your function
    image=image,  
)
def download_model(
    repo_id: str="facebook/opt-125m", # small model for testing purposes
    revision: str=None,  # include specific revision (commit hash)
    ):
    from huggingface_hub import snapshot_download

    model_path = MODEL_DIR / repo_id

    if not model_path.exists() or not any(model_path.glob("*")):  # directory exists and contains some content (files)
        print(f"Model not found at {model_path}, downloading...")

        snapshot_download(repo_id=repo_id, local_dir=model_path, revision=revision)

        print(f"Model downloaded to {model_path}")
    else:
        print(f"Model already exists at {model_path}")

    from transformers import AutoTokenizer, AutoModelForCausalLM
    import torch

    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(model_path)

    prompt = "Hello, how are you?"

    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    inputs = tokenizer.encode(prompt, return_tensors="pt")
    attention_mask = torch.ones(inputs.shape)

    output = model.generate(inputs, attention_mask=attention_mask, max_new_tokens=55, pad_token_id=tokenizer.eos_token_id)

    generated_text = tokenizer.decode(output[0], skip_special_tokens=True)
    print("Generated Text:", generated_text)