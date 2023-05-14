import json
import networkx as nx
import matplotlib.pyplot as plt

# Load dataset
with open('USAir97v2.json') as file:
    dataset = json.load(file)

# Create empty graph
G = nx.Graph()

# Add nodes (airports) to the graph with position attribute
for airport in dataset['nodes']:
    airport_code = airport['id']
    posx = airport['posx']
    posy = airport['posy']
    G.add_node(airport_code, pos=(posx, posy))

# Add edges (connections between airports) to the graph
for edge in dataset['links']:
    source = edge['source']
    target = edge['target']
    G.add_edge(source, target)

# Get positions from node attributes
pos = nx.get_node_attributes(G, 'pos')

# Draw the graph
plt.figure(figsize=(15, 10))
nx.draw(G, pos, node_size=70, node_color='cyan', edge_color='gray', width=0.3, with_labels=True)

# Show the plot
plt.show()
 