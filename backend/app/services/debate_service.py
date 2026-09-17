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
        """
        Execute a complete debate and optionally save it
        to the database.
        """

        # Validate topic
        if not topic.strip():
            raise ValueError(
                "Debate topic cannot be empty."
            )

        # Validate number of rounds
        if max_rounds not in [1, 2, 3, 5]:
            raise ValueError(
                "max_rounds must be 1, 2, 3, or 5."
            )

        # Initial LangGraph state
        initial_state = {
            "topic": topic.strip(),
            "round_number": 1,
            "max_rounds": max_rounds,
            "debate_history": [],
        }

        # Run the debate
        final_state = self.debate_graph.invoke(
            initial_state
        )

        # Save completed debate to database
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

            # Add database ID to result
            final_state["debate_id"] = debate.id

        return final_state

    def get_debate(
        self,
        debate_id: int,
        db: Session,
    ) -> dict | None:
        """
        Retrieve one complete debate from the database.
        """

        debate = (
            db.query(Debate)
            .filter(Debate.id == debate_id)
            .first()
        )

        if debate is None:
            return None

        return {
            "debate_id": debate.id,
            "topic": debate.topic,
            "rounds": debate.rounds,
            "debate_history": json.loads(
                debate.debate_history
            ),
            "research_analysis": debate.research_analysis,
            "critique": debate.critique,
            "judge_result": json.loads(
                debate.judge_result
            ),
            "created_at": debate.created_at.isoformat(),
        }

    def list_debates(
        self,
        db: Session,
    ) -> list[dict]:
        """
        Retrieve a summary of all saved debates.
        """

        debates = (
            db.query(Debate)
            .order_by(Debate.created_at.desc())
            .all()
        )

        return [
            {
                "id": debate.id,
                "topic": debate.topic,
                "rounds": debate.rounds,
                "created_at": debate.created_at.isoformat(),
            }
            for debate in debates
        ]