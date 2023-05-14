import json
import matplotlib.pyplot as plt
import networkx as nx

# Load the dataset
with open('USAir97v2.json') as file:
    dataset = json.load(file)

# Create an empty graph
G = nx.Graph()

# Add edges to the graph with attributes
for edge in dataset['links']:
    source = edge['source']
    target = edge['target']
    weight = edge['value']  # Menggunakan atribut 'value' sebagai bobot
    G.add_edge(source, target, weight=weight)

# Add nodes to the graph with attributes
for airport in dataset['nodes']:
    airport_code = airport['id']
    importance_factor = sum(edge['value'] for edge in dataset['links'] if edge['source'] == airport_code or edge['target'] == airport_code)
    G.add_node(airport_code, importance=importance_factor, id=airport['id'], name=airport['name'], city=airport['city'], country=airport['country'], posx=airport['posx'], posy=airport['posy'], latitude=airport['latitude'], longitude=airport['longitude'], state=airport['state'])

# Compute layout using spring algorithm
pos = nx.spring_layout(G)

# Draw nodes with size based on importance factor
node_sizes = [G.nodes[node]['importance'] * 10 for node in G.nodes()]
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=node_sizes)

# Draw edges with width based on weight and color based on frequency
edge_widths = [d['weight'] / 50 for u, v, d in G.edges(data=True)]
edge_colors = [d['weight'] for u, v, d in G.edges(data=True)]
nx.draw_networkx_edges(G, pos, width=edge_widths, edge_color=edge_colors, edge_cmap=plt.cm.Blues, alpha=0.8)

# Create legend
plt.scatter([], [], s=100, color='lightblue', label='Node Size: Importance Factor')
plt.scatter([], [], s=100, color='black', label='Edge Width: Weight')
plt.scatter([], [], s=100, color='red', label='Edge Color: Frequency')
plt.legend()

# Show the plot
plt.show()

