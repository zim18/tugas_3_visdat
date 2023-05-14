import json
import networkx as nx
import matplotlib.pyplot as plt

# Load dataset
with open('USAir97v2.json') as file:
    dataset = json.load(file)

# Create empty graph
G = nx.Graph()

# Add nodes (airports) to the graph with importance factor attribute
for airport in dataset['nodes']:
    airport_code = airport['id']
    importance_factor = sum(edge['value'] for edge in dataset['links'] if edge['source'] == airport_code or edge['target'] == airport_code)
    G.add_node(airport_code, importance=importance_factor)

# Add edges (connections between airports) to the graph with weight and color attributes
for edge in dataset['links']:
    source = edge['source']
    target = edge['target']
    weight = edge['value']
    color = weight / max(edge['value'] for edge in dataset['links'])
    G.add_edge(source, target, weight=weight, color=color)

# Calculate positions using force layout
pos = nx.spring_layout(G)

# Draw the graph
fig = plt.figure(figsize=(12, 8))
ax = fig.add_subplot(1, 1, 1)
ax.set_facecolor('None')
nx.draw_networkx_nodes(G, pos, node_size=[d['importance'] * 100 for n, d in G.nodes(data=True)], node_color='turquoise', ax=ax)
nx.draw_networkx_edges(G, pos, edge_color=[(d['color']*0.7, d['color']*0.7, d['color']*0.7) for u, v, d in G.edges(data=True)], width=[d['weight'] / 200 for u, v, d in G.edges(data=True)], ax=ax)
nx.draw_networkx_labels(G, pos, labels={node: node for node in G.nodes()}, font_size=8, ax=ax)

# Create legend
plt.scatter([], [], s=100, color='turquoise', label='Node Size: Importance Factor')
plt.scatter([], [], s=100, color='black', label='Edge Width: Weight')
plt.scatter([], [], s=100, color='red', label='Edge Color: Frequency')
plt.legend()

# Save plot with transparent background
plt.savefig('airports.png', bbox_inches='tight', transparent=True)

# Show the plot
plt.show()
