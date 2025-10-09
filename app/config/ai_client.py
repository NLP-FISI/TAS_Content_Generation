# app/config/ai_client.py
from openai import OpenAI, RateLimitError, APIStatusError
from app.config.settings import settings
import time

class AIClient:
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.model = settings.OPENROUTER_MODEL
        self.referer = settings.REFERER
        self.title = settings.TITLE
    
    def call(self, prompt: str, max_retries: int = 5) -> str:
        backoff = 3.0
        
        for attempt in range(1, max_retries + 1):
            try:
                resp = self.client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": self.referer,
                        "X-Title": self.title
                    },
                    extra_body={},
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": [{"type": "text", "text": prompt}]
                    }],
                )
                return resp.choices[0].message.content
                
            except RateLimitError:
                if attempt == max_retries:
                    raise Exception("Rate limit persistente después de reintentos")
                print(f"  Rate limited. Reintentando en {backoff:.1f}s…")
                time.sleep(backoff)
                backoff *= 1.8
                
            except APIStatusError as e:
                status = getattr(e, "status_code", None)
                if status in (500, 502, 503, 504) and attempt < max_retries:
                    print(f"  Error {status}. Reintentando en {backoff:.1f}s…")
                    time.sleep(backoff)
                    backoff *= 1.8
                else:
                    raise