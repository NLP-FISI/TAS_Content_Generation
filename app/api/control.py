from fastapi import APIRouter

router = APIRouter(prefix="/control")

@router.head("/status")
def check_status():
    return {"status": "ok"}
