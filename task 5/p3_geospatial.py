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
    G.add_node(airport_code, importance=importance_factor, latitude=airport['latitude'], longitude=airport['longitude'])

# Create the slider for minimum importance
min_importance_slider = FloatSlider(
    value=0,
    min=0,
    max=max(nx.get_node_attributes(G, 'importance').values()),
    step=0.1,
    description='Minimum Importance:'
)

# Create the slider for minimum weight
min_weight_slider = FloatSlider(
    value=0,
    min=0,
    max=max(nx.get_edge_attributes(G, 'weight').values()),
    step=0.1,
    description='Minimum Weight:'
)

# Update the graph based on the minimum importance and weight values
def update_graph(min_importance, min_weight):
    filtered_nodes = [node for node, importance in nx.get_node_attributes(G, 'importance').items() if importance >= min_importance]
    filtered_edges = [(source, target) for source, target, weight in G.edges(data='weight') if
                      source in filtered_nodes and target in filtered_nodes and weight >= min_weight]

    filtered_graph = G.subgraph(filtered_nodes)
    filtered_graph.remove_edges_from(list(G.edges()))
    filtered_graph.add_edges_from(filtered_edges)

    pos = {node: (G.nodes[node]['longitude'], G.nodes[node]['latitude']) for node in filtered_graph.nodes()}

    plt.figure(figsize=(10, 10))
    nx.draw_networkx(filtered_graph, pos, node_size=10, with_labels=False, alpha=0.7, width=0.5)
    plt.title('Geospatial Visualization')
    plt.axis('off')
    plt.show()

# Create the interactive visualization
interact(update_graph, min_importance=min_importance_slider, min_weight=min_weight_slider)
