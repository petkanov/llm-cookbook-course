import argparse

import modal
from openai import OpenAI

def get_completion(client, model_id, messages):
    completion_args = {
        "model": model_id,
        "stream": True,
        "messages": messages
    }
    try:
        return client.chat.completions.create(**completion_args)
    except Exception as e:
        print(f"Call to LLM failed: {e}")
        return None

TOKEN = "my-token"  # auth token, for production use, replace with a modal.Secret

workspace = modal.config._profile
app_name = "vllm-chat"
function_name = "serve"

client = OpenAI(api_key=TOKEN)
client.base_url = f"https://{workspace}--{app_name}-{function_name}.modal.run/v1"

print("Fetching active model ID...")
model = client.models.list().data[0]
model_id = model.id
print(f"Active model ID: {model_id}")

messages = [
    {
        "role": "system",
        "content": "You are lazy sarcastic angry software developer who answers with one sentence.",
    }
]

print("Type 'exit' to end chat.")
while True:
    user_input = input("Me: ")
    if user_input.lower() in ["exit"]:
        break

    MAX_CHAT_HISTORY = 30
    if len(messages) > MAX_CHAT_HISTORY:
        messages = messages[:1] + messages[-MAX_CHAT_HISTORY + 1 :]

    messages.append({"role": "user", "content": user_input})

    response = get_completion(client, model_id, messages)

    if response:
        print("GUY: ", end="")
        assistant_message = ""
        for chunk in response:
            if chunk.choices[0].delta.content:
                content = chunk.choices[0].delta.content
                print(content, end="")
                assistant_message += content
        print("\n")

        messages.append(
            {"role": "assistant", "content": assistant_message}
        )