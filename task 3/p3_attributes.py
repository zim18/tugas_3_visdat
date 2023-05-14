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
    airport_code = airport['id']  # Menggunakan atribut 'id' sebagai kode bandara
    importance_factor = sum(edge['value'] for edge in dataset['links'] if edge['source'] == airport_code or edge['target'] == airport_code)
    G.add_node(airport_code, importance=importance_factor, latitude=airport['latitude'], longitude=airport['longitude'], name=airport['name'], city=airport['city'], country=airport['country'], posx=airport['posx'], posy=airport['posy'], state=airport['state'])

# Calculate degree centrality
degree_centrality = nx.degree_centrality(G)

# Calculate betweenness centrality
betweenness_centrality = nx.betweenness_centrality(G)

# Calculate closeness centrality
closeness_centrality = nx.closeness_centrality(G)

# Print the centrality measures for each node
for node in G.nodes():
    print(f"Node: {node}")
    print(f"Degree Centrality: {degree_centrality[node]}")
    print(f"Betweenness Centrality: {betweenness_centrality[node]}")
    print(f"Closeness Centrality: {closeness_centrality[node]}")
    print()

# Visualize the centrality measures
plt.figure(figsize=(12, 4))

# Degree centrality
plt.subplot(131)
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', node_size=[v * 1000 for v in degree_centrality.values()])
nx.draw_networkx_edges(G, pos=pos, width=0.5, alpha=0.5, edge_color='gray')
plt.title('Degree Centrality')

# Betweenness centrality
plt.subplot(132)
nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', node_size=[v * 1000 for v in betweenness_centrality.values()])
nx.draw_networkx_edges(G, pos=pos, width=0.5, alpha=0.5, edge_color='gray')
plt.title('Betweenness Centrality')

# Closeness centrality
plt.subplot(133)
nx.draw_networkx_nodes(G, pos=pos, node_color='lightblue', node_size=[v * 1000 for v in closeness_centrality.values()])
nx.draw_networkx_edges(G, pos=pos, width=0.5, alpha=0.5, edge_color='gray')
plt.title('Closeness Centrality')

# Show the plot
plt.tight_layout()
plt.show()
