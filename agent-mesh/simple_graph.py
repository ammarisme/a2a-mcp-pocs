# simple_graph.py

from shared_context import ContextModel
from langgraph.graph import Graph  # adjust import if your module path differs

def build_graph():
    graph = Graph()

    # This node *may* return only a diff, so we'll merge it downstream
    def append_turn(state: dict) -> dict:
        history = state.get("conversationHistory", [])
        last_user = history[-1]["text"] if history else ""
        return {
            "conversationHistory": history + [
                {"role": "agent", "text": f"Agent got: {last_user}"}
            ]
        }

    graph.add_node("append_agent_turn", append_turn)
    graph.set_entry_point("append_agent_turn")
    graph.set_finish_point("append_agent_turn")
    return graph.compile()

_graph_app = build_graph()

def run_graph(ctx: ContextModel) -> ContextModel:
    # 1) get full dict
    original = ctx.model_dump()
    # 2) invoke node (may return only a partial update)
    result = _graph_app.invoke(original)
    # 3) merge into a new full state
    merged = {**original, **result}
    # 4) rebuild
    return ContextModel(**merged)
