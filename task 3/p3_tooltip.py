import json
import matplotlib.pyplot as plt
import networkx as nx
import mpld3

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

# Define node tooltips
node_tooltips = {}
for node in G.nodes():
    node_tooltips[node] = f"ID: {G.nodes[node]['id']}\nName: {G.nodes[node]['name']}\nCity: {G.nodes[node]['city']}\nCountry: {G.nodes[node]['country']}\nLatitude: {G.nodes[node]['latitude']}\nLongitude: {G.nodes[node]['longitude']}\nState: {G.nodes[node]['state']}"

# Visualize the graph with tooltips
fig, ax = plt.subplots(figsize=(12, 8))
pos = nx.spring_layout(G)
nx.draw_networkx_nodes(G, pos, node_color='lightblue', node_size=1000)
nx.draw_networkx_edges(G, pos, width=0.5, alpha=0.5, edge_color='gray')
nx.draw_networkx_labels(G, pos, font_size=8)
nx.draw_networkx_edge_labels(G, pos, edge_labels=nx.get_edge_attributes(G, 'weight'), font_size=6)
plt.title('Flight Connections')
plt.axis('off')
plt.margins(0.1)
plt.gca().set_aspect('equal')
plt.gca().set_ylim(-1.1, 1.1)
plt.gca().set_xlim(-1.1, 1.1)
plt.gca().set_clip_on(False)
plt.gca().set_facecolor('white')
plt.gca().set_frame_on(False)

# Add tooltips to the plot
tooltip = mpld3.plugins.PointHTMLTooltip(pos.keys(), labels=node_tooltips)
mpld3.plugins.connect(fig, tooltip)

# Show the plot
mpld3.show()

