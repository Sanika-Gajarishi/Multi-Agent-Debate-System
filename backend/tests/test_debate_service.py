from app.services.debate_service import DebateService


def test_debate_service():

    service = DebateService()

    result = service.run_debate(
        topic="Should AI replace software developers?",
        max_rounds=1,
    )

    assert isinstance(result, dict)

    assert result["topic"] == (
        "Should AI replace software developers?"
    )

    assert "pro_argument" in result
    assert "con_argument" in result

    assert "debate_history" in result

    assert len(result["debate_history"]) > 0

    assert "research_analysis" in result
    assert "critique" in result
    assert "judge_result" in result

def test_empty_topic():

    service = DebateService()

    try:
        service.run_debate(
            topic="",
            max_rounds=1,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "Debate topic cannot be empty."
        )

def test_invalid_rounds():

    service = DebateService()

    try:
        service.run_debate(
            topic="Should AI replace software developers?",
            max_rounds=4,
        )

        assert False

    except ValueError as exc:
        assert str(exc) == (
            "max_rounds must be 1, 2, 3, or 5."
        )