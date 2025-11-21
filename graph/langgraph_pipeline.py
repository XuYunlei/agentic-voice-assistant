import os, httpx
from langgraph.graph import StateGraph, END
from .schemas import GraphState
from .nodes.router import route
from .nodes.planner import plan
from .nodes.retriever import retrieve
from .nodes.answerer import answer
from .nodes.critic import critique

def build_graph():
    g = StateGraph(GraphState)
    g.add_node("router", route)
    g.add_node("planner", plan)
    g.add_node("retriever", retrieve)
    g.add_node("answerer", answer)
    g.add_node("critic", critique)

    g.set_entry_point("router")
    g.add_edge("router","planner")
    g.add_edge("planner","retriever")
    g.add_edge("retriever","answerer")
    g.add_edge("answerer","critic")
    g.add_edge("critic", END)
    return g.compile()
