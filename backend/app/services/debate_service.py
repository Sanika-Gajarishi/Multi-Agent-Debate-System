import json

from sqlalchemy.orm import Session

from app.graph.debate_graph import build_debate_graph
from app.models.debate import Debate


class DebateService:
    """
    Service responsible for executing and storing debates.
    """

    def __init__(self):
        self.debate_graph = build_debate_graph()

    def run_debate(
        self,
        topic: str,
        max_rounds: int,
        db: Session | None = None,
    ) -> dict:

        if not topic.strip():
            raise ValueError(
                "Debate topic cannot be empty."
            )

        if max_rounds not in [1, 2, 3, 5]:
            raise ValueError(
                "max_rounds must be 1, 2, 3, or 5."
            )

        initial_state = {
            "topic": topic.strip(),
            "round_number": 1,
            "max_rounds": max_rounds,
            "debate_history": [],
        }

        final_state = self.debate_graph.invoke(
            initial_state
        )

        if db is not None:
            debate = Debate(
                topic=final_state["topic"],
                rounds=final_state["max_rounds"],
                debate_history=json.dumps(
                    final_state["debate_history"]
                ),
                research_analysis=(
                    final_state["research_analysis"]
                ),
                critique=final_state["critique"],
                judge_result=json.dumps(
                    final_state["judge_result"]
                ),
            )

            db.add(debate)
            db.commit()
            db.refresh(debate)

            final_state["debate_id"] = debate.id

        return final_state