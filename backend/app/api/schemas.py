from pydantic import BaseModel, Field


class DebateRequest(BaseModel):
    topic: str = Field(
        min_length=1,
        description="The topic to debate."
    )

    rounds: int = Field(
        default=1,
        description="Number of rebuttal rounds."
    )


class DebateResponse(BaseModel):

    debate_id: int

    topic: str

    rounds: int

    debate_history: list[dict]

    research_analysis: str

    critique: str

    judge_result: dict