from fastapi import FastAPI
from compare_app.routers.vector import router as vector_router
from compare_app.routers.vectorize import router as vectorize_router

app = FastAPI(title="Vector Service")

@app.get("/health")
async def health_check():
    """
    Einfacher Health-Check, um sicherzustellen, dass der Service läuft.
    """
    return {"status": "ok"}

# Router für Distanz-Berechnung
app.include_router(
    vector_router,
    prefix="/vectors",
    tags=["vectors"]
)

# Router für Token-Vektorisierung mit wählbarem LLM
app.include_router(
    vectorize_router,
    prefix="/vectors",
    tags=["vectorization"]
)
