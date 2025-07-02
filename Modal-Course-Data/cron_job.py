import time
import modal
from datetime import datetime, timezone

GemmaModelApp = modal.Cls.from_name("gemma-webapp", "GemmaModelApp")
gemma_service = GemmaModelApp()

while True:
    reply = gemma_service.ping.remote()
    print(f"ping@{datetime.now(timezone.utc)}: {reply}")
    time.sleep(600)