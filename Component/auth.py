from fastapi import APIRouter, HTTPException
from Controller.service import generate_access_token

router = APIRouter()

@router.get("/generate-access-token")
def get_access_token(request_token: str):
    try:
        token = generate_access_token(request_token)
        return {"access_token": token}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

