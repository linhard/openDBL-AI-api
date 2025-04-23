from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

router = APIRouter()

class DistanceRequest(BaseModel):
    token_ids: List[int]

@router.post("/distance")
async def compute_distance(req: DistanceRequest):
    """
    Dummy-Implementation: gibt die übergebenen Token-IDs zurück
    und ein leeres Distanz-Array.
    """
    return {
        "token_ids": req.token_ids,
        "distances": []
    }
