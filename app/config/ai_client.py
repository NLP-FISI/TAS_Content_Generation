# app/config/ai_client.py
from openai import OpenAI, RateLimitError, APIStatusError
from app.config.settings import settings
import time
import logging

logger = logging.getLogger(__name__)

class AIClient:
    
    def __init__(self):
        self.client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=settings.OPENROUTER_API_KEY,
        )
        self.model = settings.OPENROUTER_MODEL
        self.referer = settings.REFERER
        self.title = settings.TITLE
        
        self.delay_between_calls = settings.DELAY_BETWEEN_API_CALLS
    
    def call(self, prompt: str, max_retries: int = 5) -> str:
        backoff = 3.0
        
        for attempt in range(1, max_retries + 1):
            try:
                logger.debug(f"AIClient: Intento {attempt}/{max_retries} - Enviando prompt...")
                
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
                
                response_text = resp.choices[0].message.content
                logger.debug(f"AIClient: Respuesta recibida. Esperando {self.delay_between_calls}s antes de siguiente llamada...")
                time.sleep(self.delay_between_calls)
                
                return response_text
                
            except RateLimitError:
                if attempt == max_retries:
                    logger.error("Rate limit persistente después de reintentos")
                    raise Exception("Rate limit persistente después de reintentos")
                
                logger.warning(f"Rate limit detectado. Reintentando en {backoff:.1f}s (intento {attempt}/{max_retries})…")
                time.sleep(backoff)
                backoff *= 1.8
                
            except APIStatusError as e:
                status = getattr(e, "status_code", None)
                
                if status in (500, 502, 503, 504) and attempt < max_retries:
                    logger.warning(f"Error {status} del servidor. Reintentando en {backoff:.1f}s…")
                    time.sleep(backoff)
                    backoff *= 1.8
                else:
                    logger.error(f"Error API {status}: {str(e)}")
                    raise
            
            except Exception as e:
                logger.error(f"Error inesperado en AIClient: {str(e)}")
                raise