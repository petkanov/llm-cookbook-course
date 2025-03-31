import modal
from modal import App, Image

app = App("gemma-webapp")
image = (
    Image.debian_slim()
    .apt_install("git")
    .pip_install("torch", "transformers", "huggingface_hub", "fastapi[standard]", "accelerate")
    .run_commands("git config --global credential.helper store")
)
secrets = [modal.Secret.from_name("hf-token")]

@app.cls(image=image, secrets=secrets, gpu="T4", container_idle_timeout=1200)
class GemmaModelApp:
    @modal.enter()
    def startup(self):
        import os, torch
        from transformers import AutoTokenizer, AutoModelForCausalLM
        from huggingface_hub import login

        hf_token = os.environ['HF_TOKEN']
        login(hf_token, add_to_git_credential=True)

        print("Loading tokenizer...")
        self.tokenizer = AutoTokenizer.from_pretrained("google/gemma-2-2b-it")
        print("Loading model...")
        self.model = AutoModelForCausalLM.from_pretrained("google/gemma-2-2b-it", device_map="auto")

        self.tokenizer.pad_token = self.tokenizer.eos_token
        self.tokenizer.padding_side = "right" 

        print("Model loaded successfully!")

    @modal.method()
    def ping(self):
        from datetime import datetime, timezone
        return f"pong@{datetime.now(timezone.utc)}"
        
    @modal.method()
    def generate(self, prompt: str) -> str:
        print(f"Received prompt: {prompt}")
        return self._generate_response(prompt)

    @modal.web_endpoint(method="POST", docs=True)
    def web_generate(self, prompt: str) -> str:
        print(f"[Updated] Web Controller Received prompt: {prompt}")
        return self._generate_response(prompt)
    
    def _generate_response(self, prompt: str) -> str:
        import torch
        
        inputs = self.tokenizer.encode(prompt, return_tensors="pt").to("cuda")
        attention_mask = torch.ones(inputs.shape, device="cuda")
        outputs = self.model.generate(
            inputs,
            attention_mask=attention_mask,
            max_new_tokens=15,     # Generate up to 100 tokens
            num_return_sequences=1, # Ensures that the model generates only one response. Increase this number if you want the model to generate multiple variations of the response.
            do_sample=True,         # Enables sampling of (temperature, top_k, top_p) parameters for more diverse responses
            temperature=0.7,        # Controls randomness (lower is more deterministic)
            top_k=50,               # Only considers the top 50 tokens with the highest probabilities
            top_p=0.9,              # Implements nucleus sampling for more diverse and natural responses.
        )

        return self.tokenizer.decode(outputs[0], skip_special_tokens=False)