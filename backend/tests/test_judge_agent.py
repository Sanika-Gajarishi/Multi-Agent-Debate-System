from app.agents.judge_agent import JudgeAgent


def test_judge_agent():

    agent = JudgeAgent()

    topic = "Should AI replace software developers?"

    debate_history = """
    ROUND: 0
    SPEAKER: PRO
    TYPE: opening

    AI can automate repetitive programming tasks
    and generate code quickly.


    ROUND: 0
    SPEAKER: CON
    TYPE: opening

    AI cannot completely replace developers because
    software development requires human judgment.


    ROUND: 1
    SPEAKER: PRO
    TYPE: rebuttal

    AI can assist developers and increase productivity.


    ROUND: 1
    SPEAKER: CON
    TYPE: rebuttal

    Human oversight remains important.
    """

    research_analysis = """
    Both arguments contain factual claims that
    require supporting evidence.
    """

    critique = """
    The Pro argument assumes that automation leads
    directly to complete replacement.

    The Con argument makes broad claims about human
    judgment without sufficient evidence.
    """

    result = agent.judge_debate(
        topic=topic,
        debate_history=debate_history,
        research_analysis=research_analysis,
        critique=critique,
    )

    assert isinstance(result, dict)

    assert result["winner"] in [
        "PRO",
        "CON",
        "DRAW",
    ]

    assert 0 <= result["pro_score"] <= 100
    assert 0 <= result["con_score"] <= 100

    assert 0 <= result["confidence"] <= 1

    assert len(result["strongest_pro_argument"]) > 0
    assert len(result["strongest_con_argument"]) > 0
    assert len(result["reasoning"]) > 0
    assert len(result["final_verdict"]) > 0


    