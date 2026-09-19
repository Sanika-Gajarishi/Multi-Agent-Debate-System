from app.agents.pro_agent import ProAgent


def test_pro_agent(monkeypatch):

    agent = ProAgent()

    def fake_generate(system_prompt, user_prompt):
        return "This is a test Pro argument."

    monkeypatch.setattr(
        agent.llm,
        "generate",
        fake_generate,
    )

    topic = "Should AI replace software developers?"

    argument = agent.generate_argument(topic)

    assert argument is not None
    assert len(argument) > 0