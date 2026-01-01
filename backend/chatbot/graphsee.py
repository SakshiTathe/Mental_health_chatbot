import pickle
import networkx as nx
import matplotlib.pyplot as plt

with open("user_knowledge_graph.gpickle", "rb") as f:
    G = pickle.load(f)
print(G.nodes())
for node, data in G.nodes(data=True):
    print(node, data)
print(G.edges())
for u, v, data in G.edges(data=True):
    print(u, "->", v, data)

plt.figure(figsize=(8,6))
nx.draw(G, with_labels=True, node_color='skyblue', font_size=8, node_size=800)
labels = nx.get_node_attributes(G, 'type')
nx.draw(G, labels=labels, with_labels=True)
plt.show()

