from app.agents.con_agent import ConAgent


def test_con_agent(monkeypatch):

    agent = ConAgent()

    def fake_generate(system_prompt, user_prompt):
        return "This is a test Con argument."

    monkeypatch.setattr(
        agent.llm,
        "generate",
        fake_generate,
    )

    topic = "Should AI replace software developers?"

    argument = agent.generate_argument(topic)

    assert argument is not None
    assert len(argument) > 0