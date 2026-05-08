from __future__ import annotations

from langgraph.graph import END, StateGraph

from agent.agent1.graph import agent1_graph
from agent.agent2.graph import agent2_graph
from agent.agent3.graph import agent3_graph
from models.schema import AgentState


def _run_agent1(state: AgentState) -> dict:
    result = agent1_graph.invoke(state)
    return {
        "collected_data": result.get("collected_data"),
        "errors": result.get("errors", []),
    }


def _run_agent2(state: AgentState) -> dict:
    result = agent2_graph.invoke(state)
    return {
        "collected_data": result.get("collected_data"),  # filter_noise may update this
        "hypotheses": result.get("hypotheses"),
        "errors": result.get("errors", []),
    }


def _run_agent3(state: AgentState) -> dict:
    result = agent3_graph.invoke(state)
    return {
        "report": result.get("report"),
        "errors": result.get("errors", []),
    }


def _route_after_agent1(state: AgentState) -> str:
    if state.get("errors"):
        return END
    return "agent2"


def _route_after_agent2(state: AgentState) -> str:
    if state.get("errors"):
        return END
    return "agent3"


def build_pipeline():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent1", _run_agent1)
    workflow.add_node("agent2", _run_agent2)
    workflow.add_node("agent3", _run_agent3)

    workflow.set_entry_point("agent1")
    workflow.add_conditional_edges(
        "agent1",
        _route_after_agent1,
        {"agent2": "agent2", END: END},
    )
    workflow.add_conditional_edges(
        "agent2",
        _route_after_agent2,
        {"agent3": "agent3", END: END},
    )
    workflow.add_edge("agent3", END)

    return workflow.compile()


pipeline = build_pipeline()
