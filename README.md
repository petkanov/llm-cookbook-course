# LLM Deployment Course

A production-ready platform for deploying and serving Large Language Models (LLMs) using Modal cloud infrastructure. This project provides a complete solution for downloading, deploying, and serving various LLMs with an OpenAI-compatible API interface.

## 🌟 Features

- 🚀 Easy deployment of LLMs using Modal
- 💨 Efficient model serving using vLLM
- 🔄 OpenAI-compatible API interface
- 📦 Model quantization support (4-bit)
- 🔧 Concurrent request handling (up to 1000 requests)
- 🏪 Persistent model storage using Modal volumes
- 🤗 HuggingFace integration
- 🔌 FastAPI-based endpoints

## 📋 Prerequisites

- Python 3.10+
- Modal account and CLI setup
- HuggingFace account (for model access)

## 🛠️ Installation

### 1. Environment Setup

Choose one of the following methods:

#### Using Conda (with environment.yml)
```bash
conda env create -f environment.yml
conda activate [environment_name]
```

#### Using Conda (manual)
```bash
conda create -p venv python==3.12
conda activate venv/
```

#### Using Python venv
```bash
python -m venv myenv
myenv/Scripts/activate  # Windows
source myenv/bin/activate  # Linux/Mac
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```


## 🚀 Deployment

### 1. Set up Modal Secrets

Create a HuggingFace token secret:
```bash
modal secret create hf-token --env HF_TOKEN=your_huggingface_token
```

### 2. Download Model

Deploy the model download service:
```bash
modal deploy chat-app/download-model-service.py
```

### 3. Deploy Inference Service

Deploy the vLLM inference service:
```bash
modal deploy chat-app/inferencing-service.py
```

## 💻 Usage

### Using the CLI Client

```bash
python client_openai.py --prompt "Your prompt here" \
    --model "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16" \
    --temperature 0.7 \
    --max-tokens 500
```

### Using the Web API

Send a POST request to the web endpoint:
```bash
curl -X POST "https://your-modal-endpoint/generate" \
     -H "Content-Type: application/json" \
     -d '{"prompt": "Your prompt here"}'
```

## ⚙️ Configuration

### Model Configuration

Default model settings in `inferencing-service.py`:
```python
MODEL_REPO_ID = "neuralmagic/Meta-Llama-3.1-8B-Instruct-quantized.w4a16"
N_GPU = 1  # Number of GPUs
```

### API Configuration

- Default concurrent requests: 1000
- Container idle timeout: 5 minutes
- Function timeout: 24 hours

## 🔒 Security

- API authentication using tokens (configurable)
- HuggingFace token required for model access
- Secure model storage using Modal volumes

## 🔧 Advanced Configuration

### Custom Model Deployment

To deploy a different model:

1. Update the `MODEL_REPO_ID` in `download-model-service.py`
2. Update GPU requirements if needed
3. Adjust quantization settings if required

### Scaling Configuration

Modify in `inferencing-service.py`:
```python
N_GPU = 1  # Increase for more processing power
allow_concurrent_inputs=1000  # Adjust based on needs
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Troubleshooting

### Common Issues

1. **Model Access Errors**
   ```
   Cannot access gated repo for url https://huggingface.co/...
   ```
   Solution: Accept model terms on HuggingFace website

2. **GPU Memory Issues**
   - Reduce batch size
   - Use model quantization
   - Increase GPU count

## 📚 Additional Resources

- [Modal Documentation](https://modal.com/docs)
- [vLLM Documentation](https://vllm.ai/)
- [HuggingFace Documentation](https://huggingface.co/docs)
