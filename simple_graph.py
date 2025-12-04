from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import TypedDict

# create class


class PortfolioState(TypedDict):
    amount_usd: float
    total_usd: float
    total_inr: float


# create object
"""
my_obj . PortfolioState = {
    'amount_usd':1000,
    'total_usd':100,
    'total_inr':100
}
"""

#   Creating state


def calc_total(state: PortfolioState) -> PortfolioState:
    state['total_usd'] = state['amount_usd']*1.08
    return state


def convert_to_inr(state: PortfolioState) -> PortfolioState:
    state['total_inr'] = state['total_usd'] * 85
    return state


# import graph
# create graph
builder = StateGraph(PortfolioState)
builder.add_node("calc_total_node", calc_total)
builder.add_node("calc_inr_node", convert_to_inr)

builder.add_edge(START, "calc_total_node")
builder.add_edge("calc_total_node", "calc_inr_node")
builder.add_edge("calc_inr_node", END)

# compile graph
graph = builder.compile()

# display graph
#display(Image(graph.get_graph().draw_mermaid_png()))
png_bytes = graph.get_graph().draw_mermaid_png()

with open("graph_output.png", "wb") as f:
    f.write(png_bytes)

print("Graph saved as graph_output.png")

