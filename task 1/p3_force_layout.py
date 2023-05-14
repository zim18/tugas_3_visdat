import pandas as pd
import networkx as nx
import matplotlib as plt

# Load the dataset
data = pd.read_excel('USAir97.xlsx')

# Create a graph
G = nx.Graph()

# Add nodes
for i in range(len(data)):
    G.add_node(data['city'][i])
    G.add_node(data['city'][i])

# Add edges
for i in range(len(data)):
    G.add_edge(data['city'][i], data['city'][i])

# Generate the layout
pos = nx.spring_layout(G)

# Draw the graph
nx.draw(G, pos=pos)

# Define the labels
labels = {node: node for node in G.nodes()}

# Define the edge colors and sizes
edge_colors = [1 for edge in G.edges()]
edge_sizes = [1 for edge in G.edges()]

# Draw the graph with labels and adjusted edges
nx.draw_networkx(G, pos=pos, labels=labels, edge_color=edge_colors, width=edge_sizes)
