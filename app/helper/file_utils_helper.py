# app/helpers/file_utils.py
import json
import time
from pathlib import Path
from typing import Any

class FileUtils:
    
    @staticmethod
    def ensure_outputs_dir() -> Path:
        p = Path("outputs")
        p.mkdir(parents=True, exist_ok=True)
        return p
    
    @staticmethod
    def now_tag() -> str:
        return time.strftime("%Y%m%d_%H%M%S")
    
    @staticmethod
    def save_json(data: Any, filename: str) -> Path:
        outdir = FileUtils.ensure_outputs_dir()
        filepath = outdir / filename
        filepath.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8"
        )
        return filepath