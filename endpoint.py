import modal
from modal import App, Image

app = App(image = Image.debian_slim().pip_install("fastapi[standard]"))

@app.function()
@modal.web_endpoint(docs=True)
def greet(user: str) -> str:
    return f"Hello {user}!"

@app.function()
@modal.web_endpoint(method="POST", docs=True)
def square(item: dict):
    return {"value": item['x']**2}