import json
import matplotlib.pyplot as plt
import networkx as nx
from ipywidgets import interact, FloatSlider
from IPython.display import display

# Load the dataset
with open('USAir97v2.json') as file:
    dataset = json.load(file)

# Create an empty graph
G = nx.Graph()

# Add edges to the graph with attributes
for edge in dataset['links']:
    source = edge['source']
    target = edge['target']
    weight = edge['value']
    G.add_edge(source, target, weight=weight)

# Add nodes to the graph with attributes
for airport in dataset['nodes']:
    airport_code = airport['id']
    importance_factor = sum(edge['value'] for edge in dataset['links'] if
                            edge['source'] == airport_code or edge['target'] == airport_code)
    G.add_node(airport_code, importance=importance_factor)

# Create the slider for minimum importance
min_importance_slider = FloatSlider(
    value=0,
    min=0,
    max=max(nx.get_node_attributes(G, 'importance').values()),
    step=0.1,
    description='Minimum Importance:'
)

# Update the graph based on the minimum importance value
def update_graph(min_importance):
    filtered_nodes = [node for node, importance in nx.get_node_attributes(G, 'importance').items() if importance >= min_importance]
    filtered_edges = [(source, target) for source, target in G.edges if source in filtered_nodes and target in filtered_nodes]

    filtered_graph = G.subgraph(filtered_nodes)
    filtered_graph.remove_edges_from(list(G.edges) + [(target, source) for source, target in G.edges if source not in filtered_nodes or target not in filtered_nodes])

    plt.figure(figsize=(10, 6))
    pos = nx.spring_layout(filtered_graph)
    nx.draw_networkx(filtered_graph, pos=pos, node_color='lightblue', node_size=50, edge_color='gray', with_labels=True)
    plt.title('Force Layout')
    plt.show()

# Display the slider and graph
display(min_importance_slider)
interact(update_graph, min_importance=min_importance_slider)
