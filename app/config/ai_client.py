from openai import OpenAI, RateLimitError, APIStatusError
from app.config.settings import settings
import time
import logging
from typing import Optional

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
        self.last_call_time = 0
    
    def _wait_if_needed(self):
        elapsed = time.time() - self.last_call_time
        if elapsed < self.delay_between_calls:
            wait_time = self.delay_between_calls - elapsed
            logger.debug(f"Esperando {wait_time:.1f}s antes de siguiente llamada...")
            time.sleep(wait_time)
        self.last_call_time = time.time()
    
    def call(self, prompt: str, max_retries: int = 5) -> str:
        backoff = 2.0
        max_backoff = 120.0 
        
        for attempt in range(1, max_retries + 1):
            try:
                self._wait_if_needed()
                logger.debug(f"AIClient: Intento {attempt}/{max_retries} - Enviando prompt...")
                
                resp = self.client.chat.completions.create(
                    extra_headers={
                        "HTTP-Referer": self.referer,
                        "X-Title": self.title
                    },
                    model=self.model,
                    messages=[{
                        "role": "user",
                        "content": prompt
                    }],
                    temperature=0.7
                )
                
                response_text = resp.choices[0].message.content
                logger.debug(f"AIClient: Respuesta recibida")
                
                return response_text
                
            except RateLimitError as e:
                if attempt == max_retries:
                    logger.error(f"Rate limit persistente después de {max_retries} reintentos")
                    raise Exception(f"Rate limit persistente: {str(e)}")
                
                wait_time = min(backoff, max_backoff)
                logger.warning(f"⏱️  Rate limit detectado. Esperando {wait_time:.1f}s (intento {attempt}/{max_retries})…")
                time.sleep(wait_time)
                backoff = min(backoff * 2, max_backoff)
                
            except APIStatusError as e:
                status = getattr(e, "status_code", None)
                
                if status in (429, 500, 502, 503, 504) and attempt < max_retries:
                    wait_time = min(backoff, max_backoff)
                    logger.warning(f"Error {status} del servidor. Esperando {wait_time:.1f}s…")
                    time.sleep(wait_time)
                    backoff = min(backoff * 2, max_backoff)
                else:
                    logger.error(f"Error API {status}: {str(e)}")
                    raise
            
            except Exception as e:
                logger.error(f"Error inesperado en AIClient: {str(e)}")
                raise