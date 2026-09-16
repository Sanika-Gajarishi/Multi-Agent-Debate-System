from fastapi import FastAPI
from app.storage.database import Base, engine
from app.models.debate import Debate
from app.api.routes import router


app = FastAPI(
    title="Multi-Agent Debate System",
    description=(
        "AI-powered multi-agent debate system "
        "using Gemini and LangGraph."
    ),
    version="1.0.0",
)

Base.metadata.create_all(bind=engine)

app.include_router(router)


@app.get("/")
def root():

    return {
        "message": "Multi-Agent Debate System API",
        "status": "running",
    }


@app.get("/health")
def health_check():

    return {
        "status": "healthy"
    }