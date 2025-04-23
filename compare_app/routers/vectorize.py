from fastapi import APIRouter
from pydantic import BaseModel
from typing import List

# ➡️ Hier definieren wir den APIRouter
router = APIRouter()

class VectorizeRequest(BaseModel):
    tokens: List[str]
    llm: str

@router.post("/vectorize")
async def vectorize_tokens(req: VectorizeRequest):
    """
    Dummy-Implementation: übernimmt tokens und llm,
    liefert eine leere Vektor-Liste zurück.
    """
    return {
        "tokens": req.tokens,
        "llm": req.llm,
        "vectors": []
    }
