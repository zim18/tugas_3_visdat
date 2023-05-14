import json
import matplotlib.pyplot as plt
import networkx as nx
import ipywidgets as widgets
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
    G.add_node(airport_code, importance=importance_factor, pos=(airport['posx'], airport['posy']))

# Define the filtering function
def apply_filter(min_importance, min_weight):
    filtered_nodes = [node for node, data in G.nodes(data=True) if data['importance'] >= min_importance]
    filtered_edges = [(source, target) for source, target, data in G.edges(data=True) if data['weight'] >= min_weight]
    filtered_graph = G.copy()  # Create a mutable copy of the original graph
    filtered_graph.remove_edges_from(list(filtered_graph.edges - set(filtered_edges)))

    # Plot the filtered graph
    plt.figure(figsize=(10, 10))
    pos = nx.get_node_attributes(filtered_graph, 'pos')
    missing_nodes = set(filtered_nodes) - set(pos.keys())
    missing_pos = {node: (0, 0) for node in missing_nodes}
    pos.update(missing_pos)
    nx.draw(filtered_graph, pos, with_labels=True, node_size=50, node_color='lightblue', edge_color='gray')
    plt.title('Filtered Graph')
    plt.show()

# Create the slider for minimum importance
min_importance_slider = FloatSlider(
    value=0,
    min=0,
    max=max(data['importance'] for _, data in G.nodes(data=True)),
    description='Minimum Importance:',
    step=0.1
)

# Create the slider for minimum weight
min_weight_slider = FloatSlider(
    value=0,
    min=0,
    max=max(data['weight'] for _, _, data in G.edges(data=True)),
    description='Minimum Weight:',
    step=0.01
)

# Create the output widget
output = widgets.Output()

# Define the update function
def update_filtering(min_importance, min_weight):
    with output:
        output.clear_output()
        apply_filter(min_importance, min_weight)


# Set up the interactivity
interact(update_filtering, min_importance=min_importance_slider.value, min_weight=min_weight_slider.value)

# Display the sliders and output widget
display(min_importance_slider, min_weight_slider, output)

# # Apply the initial filter
# apply_filter(min_importance_slider.value, min_weight_slider.value)
