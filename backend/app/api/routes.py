from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from anthropic import APIError, RateLimitError

from app.api.schemas import (
    DebateRequest,
    DebateResponse,
    DebateSummary,
    DebateDetailResponse,
)
from app.services.debate_service import DebateService
from app.storage.database import get_db


router = APIRouter(
    prefix="/api",
    tags=["Debate"],
)


debate_service = DebateService()


# ============================================================
# CREATE AND RUN DEBATE
# ============================================================

@router.post(
    "/debate",
    response_model=DebateResponse,
)
def run_debate(
    request: DebateRequest,
    db: Session = Depends(get_db),
):
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

    except RateLimitError:
        raise HTTPException(
            status_code=429,
            detail=(
                "Anthropic API quota or rate limit exceeded. "
                "Please try again later or check your API usage."
            ),
        )

    except APIError:
        raise HTTPException(
            status_code=502,
            detail="Anthropic API request failed.",
        )


# ============================================================
# LIST ALL DEBATES
# ============================================================

@router.get(
    "/debates",
    response_model=list[DebateSummary],
)
def list_debates(
    db: Session = Depends(get_db),
):
    return debate_service.list_debates(
        db=db,
    )


# ============================================================
# GET SINGLE DEBATE
# ============================================================

@router.get(
    "/debates/{debate_id}",
    response_model=DebateDetailResponse,
)
def get_debate(
    debate_id: int,
    db: Session = Depends(get_db),
):
    result = debate_service.get_debate(
        debate_id=debate_id,
        db=db,
    )

    if result is None:
        raise HTTPException(
            status_code=404,
            detail="Debate not found.",
        )

    return result