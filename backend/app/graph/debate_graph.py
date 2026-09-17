from typing import TypedDict

from langgraph.graph import StateGraph, START, END

from app.agents.pro_agent import ProAgent
from app.agents.con_agent import ConAgent
from app.agents.research_agent import ResearchAgent
from app.agents.critic_agent import CriticAgent
from app.agents.judge_agent import JudgeAgent


class DebateState(TypedDict, total=False):
    topic: str

    # Opening arguments

    round_number: int
    max_rounds: int

    pro_argument: str
    con_argument: str

    # Rebuttal round
    pro_rebuttal: str
    con_rebuttal: str

    debate_history: list[dict]

    # Analysis
    research_analysis: str
    critique: str

    # Final decision
    judge_result: dict

def append_history(
    state: DebateState,
    speaker: str,
    statement_type: str,
    content: str,
    round_number: int,
) -> list[dict]:

    history = list(state.get("debate_history", []))

    history.append(
        {
            "round": round_number,
            "speaker": speaker,
            "type": statement_type,
            "content": content,
        }
    )

    return history

def format_debate_history(state: DebateState) -> str:

    history = state.get("debate_history", [])

    formatted = []

    for item in history:
        formatted.append(
            f"""
ROUND: {item["round"]}
SPEAKER: {item["speaker"]}
TYPE: {item["type"]}

{item["content"]}
"""
        )

    return "\n".join(formatted)

def pro_node(state: DebateState) -> dict:
    agent = ProAgent()

    argument = agent.generate_argument(
        state["topic"]
    )

    history = append_history(
        state=state,
        speaker="PRO",
        statement_type="Opening Argument",
        content=argument,
        round_number=0
    )

    return {
        "pro_argument": argument,
        "debate_history": history
    }


def con_node(state: DebateState) -> dict:
    agent = ConAgent()

    argument = agent.generate_argument(
        state["topic"]
    )

    history = append_history(
        state=state,
        speaker="CON",
        statement_type="Opening Argument",
        content=argument,
        round_number=0
    )

    return {
        "con_argument": argument,
        "debate_history": history
    }

def pro_rebuttal_node(state: DebateState) -> dict:
    agent = ProAgent()

    debate_history = format_debate_history(state)

    rebuttal = agent.generate_rebuttal(
        topic=state["topic"],
        con_argument=state["con_argument"],
    )

    history = append_history(
        state=state,
        speaker="PRO",
        statement_type="Rebuttal",
        content=rebuttal,
        round_number=state["round_number"],
    )

    return {
        "pro_rebuttal": rebuttal,
        "debate_history": history
    }

def con_rebuttal_node(state: DebateState) -> dict:
    agent = ConAgent()

    debate_history = format_debate_history(state)

    rebuttal = agent.generate_rebuttal(
        topic=state["topic"],
        pro_argument=debate_history,
           
    )
    history = append_history(
        state=state,
        speaker="CON",
        statement_type="Rebuttal",
        content=rebuttal,
        round_number=state["round_number"],
    )

    return {
        "con_rebuttal": rebuttal,
        "debate_history": history,
        "round_number": state["round_number"] + 1,
    }

def research_node(state: DebateState) -> dict:
    agent = ResearchAgent()

    debate_history = format_debate_history(state)

    analysis = agent.analyze_debate(
        topic=state["topic"],
        debate_history=debate_history,
        
    )

    return {
        "research_analysis": analysis
    }


def critic_node(state: DebateState) -> dict:
    agent = CriticAgent()

    debate_history = format_debate_history(state)

    critique = agent.critique_debate(
        topic=state["topic"],
        debate_history=debate_history,
        research_analysis=state["research_analysis"],
        
    )

    return {
        "critique": critique
    }


def judge_node(state: DebateState) -> dict:
    agent = JudgeAgent()

    debate_history = format_debate_history(state)

    result = agent.judge_debate(
        topic=state["topic"],
        debate_history=debate_history,
        research_analysis=state["research_analysis"],
        critique=state["critique"],
    )

    return {
        "judge_result": result
    }

def route_after_con_rebuttal(state: DebateState) -> str:

    if state["round_number"] <= state["max_rounds"]:
        return "pro_rebuttal"

    return "research"

def build_debate_graph():

    graph = StateGraph(DebateState)

    graph.add_node("pro", pro_node)
    graph.add_node("con", con_node)

    graph.add_node(
        "pro_rebuttal",
        pro_rebuttal_node
    )

    graph.add_node(
        "con_rebuttal",
        con_rebuttal_node
    )

    graph.add_node(
        "research",
        research_node
    )

    graph.add_node(
        "critic",
        critic_node
    )

    graph.add_node(
        "judge",
        judge_node
    )

    graph.add_edge(
        START,
        "pro"
    )

    graph.add_edge(
        "pro",
        "con"
    )

    graph.add_edge(
        "con",
        "pro_rebuttal"
    )

    graph.add_edge(
        "pro_rebuttal",
        "con_rebuttal"
    )

    graph.add_conditional_edges(
        "con_rebuttal",
        route_after_con_rebuttal,
        {
            "pro_rebuttal": "pro_rebuttal",
            "research": "research",
        },
    )

    graph.add_edge(
        "research",
        "critic"
    )

    graph.add_edge(
        "critic",
        "judge"
    )

    graph.add_edge(
        "judge",
        END
    )

    return graph.compile()

    