from fastapi import FastAPI
from ontology_app.routers import ontology

app = FastAPI(title="Ontology Service")
app.include_router(ontology.router, prefix="/ontologies", tags=["ontologies"])
