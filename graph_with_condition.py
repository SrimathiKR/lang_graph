from langgraph.graph import StateGraph, START, END
from IPython.display import Image, display
from typing import TypedDict, Literal

# create class


class PortfolioState(TypedDict):
    amount_usd: float
    total_usd:float
    target_currency: Literal["INR", "EUR"]
    total: float


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
    state['total'] = state['total_usd'] * 85
    return state


def convert_to_eur(state: PortfolioState) -> PortfolioState:
    state['total'] = state['total_usd'] * 0.8
    return state


def choose_currency(state: PortfolioState) -> str:
    return state["target_currency"]


# import graph
# create graph
builder = StateGraph(PortfolioState)
builder.add_node("calc_total_node", calc_total)
#builder.add_node("choose_currency", choose_currency)
builder.add_node("calc_inr_node", convert_to_inr)
builder.add_node("calc_eur_node", convert_to_eur)

# change happens here for condition

builder.add_edge(START, "calc_total_node")
builder.add_conditional_edges(
    "calc_total_node",
    choose_currency,
    {
        "INR": "calc_inr_node",
        "EUR": "calc_eur_node"
    })
builder.add_edge("calc_inr_node", END)
builder.add_edge("calc_eur_node", END)

# compile graph
graph = builder.compile()

# display graph
# display(Image(graph.get_graph().draw_mermaid_png()))
png_bytes = graph.get_graph().draw_mermaid_png()

with open("conditional_graph_output.png", "wb") as f:
    f.write(png_bytes)

print("Graph saved as graph_output.png")
# invoking values to the graph
print(graph.invoke({'amount_usd': 1000, 'target_currency': "INR"}))
