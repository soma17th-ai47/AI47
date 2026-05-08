from __future__ import annotations

from langgraph.graph import END, StateGraph

from agent.agent1.graph import agent1_graph
from models.schema import AgentState


def _run_agent1(state: AgentState) -> dict:
    result = agent1_graph.invoke(state)
    return {
        "collected_data": result.get("collected_data"),
        "errors": result.get("errors", []),
    }


def _route_after_agent1(state: AgentState) -> str:
    if state.get("errors"):
        return END
    return "agent2"


def _agent2_placeholder(state: AgentState) -> dict:
    # Agent 2 담당자 구현 후 교체
    return {"hypotheses": []}


def _agent3_placeholder(state: AgentState) -> dict:
    # Agent 3 담당자 구현 후 교체
    return {"report": {}}


def build_pipeline():
    workflow = StateGraph(AgentState)

    workflow.add_node("agent1", _run_agent1)
    workflow.add_node("agent2", _agent2_placeholder)
    workflow.add_node("agent3", _agent3_placeholder)

    workflow.set_entry_point("agent1")
    workflow.add_conditional_edges(
        "agent1",
        _route_after_agent1,
        {"agent2": "agent2", END: END},
    )
    workflow.add_edge("agent2", "agent3")
    workflow.add_edge("agent3", END)

    return workflow.compile()


pipeline = build_pipeline()
