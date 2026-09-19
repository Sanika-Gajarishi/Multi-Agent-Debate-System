from app.agents.critic_agent import CriticAgent


def test_critic_agent(monkeypatch):

    agent = CriticAgent()

    def fake_generate(system_prompt, user_prompt):
        return "This is a test debate critique."

    monkeypatch.setattr(
        agent.llm,
        "generate",
        fake_generate,
    )

    topic = "Should AI replace software developers?"

    debate_history = """
    ROUND: 0
    SPEAKER: PRO
    TYPE: opening

    AI can automate repetitive programming tasks.

    ROUND: 0
    SPEAKER: CON
    TYPE: opening

    Human judgment is still required.

    ROUND: 1
    SPEAKER: PRO
    TYPE: rebuttal

    AI can assist developers but also increase productivity.

    ROUND: 1
    SPEAKER: CON
    TYPE: rebuttal

    Human oversight remains important.
    """

    research_analysis = """
    Both arguments contain factual claims
    that require supporting evidence.
    """

    critique = agent.critique_debate(
        topic=topic,
        debate_history=debate_history,
        research_analysis=research_analysis,
    )

    assert critique is not None
    assert len(critique) > 0