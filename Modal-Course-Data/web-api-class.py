import modal
from modal import App, Image

app = App("web-app", image = Image.debian_slim().pip_install("fastapi[standard]") )

@app.cls(cpu=1, memory="1Gi")
class WebApp:
    @modal.enter()
    def startup(self):
        from datetime import datetime, timezone

        print("Container started -> Start up time initiated!")
        self.start_time = datetime.now(timezone.utc)

    @modal.method()
    def ping(self):
        return "pong"

    @modal.web_endpoint(docs=True)
    def web(self):
        from datetime import datetime, timezone

        current_time = datetime.now(timezone.utc)
        return {"start_time": self.start_time, "current_time": current_time}