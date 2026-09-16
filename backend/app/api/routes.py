import json
from fastapi import APIRouter,Depends,  HTTPException
from sqlalchemy.orm import Session

from app.api.schemas import (
    DebateRequest,
    DebateResponse,
)

from app.services.debate_service import DebateService
from app.storage.database import get_db

router = APIRouter(
    prefix="/api",
    tags=["Debate"],
)


debate_service = DebateService()


@router.post(
    "/debate",
    response_model=DebateResponse,
)
def run_debate(request: DebateRequest, db: Session = Depends(get_db)):

    try:

        result = debate_service.run_debate(
            topic=request.topic,
            max_rounds=request.rounds,
            db=db,
        )

        return DebateResponse(
            debate_id=result["debate_id"],
            topic=result["topic"],
            rounds=result["max_rounds"],
            debate_history=result["debate_history"],
            research_analysis=result["research_analysis"],
            critique=result["critique"],
            judge_result=result["judge_result"],
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )