import streamlit as st
import networkx as nx
import matplotlib.pyplot as plt

# Title
st.title("Resilient Graph Network - Emotional Support System")

# Initialize graph
G = nx.Graph()

# Sidebar for user input
st.sidebar.header("Add Nodes and Edges")

# Add nodes
nodes = st.sidebar.text_input("Enter nodes (comma separated)", "A,B,C,D").split(",")
G.add_nodes_from([n.strip() for n in nodes])

# Add edges
edge_input = st.sidebar.text_area("Enter edges (format: node1,node2,weight,resilience)", 
                                  "A,B,3,2\nA,C,2,1\nB,C,2,2\nB,D,5,3\nC,D,4,2")

edges = []
for line in edge_input.strip().split("\n"):
    try:
        n1, n2, w, r = line.split(",")
        G.add_edge(n1.strip(), n2.strip(), weight=int(w), resilience=int(r))
    except:
        pass

# Function to calculate resilient path
def resilient_path(G, source, target):
    for u, v, data in G.edges(data=True):
        data["effective"] = data["weight"] - data["resilience"]
    try:
        return nx.dijkstra_path(G, source, target, weight="effective")
    except nx.NetworkXNoPath:
        return None

# User chooses source and target
source = st.sidebar.selectbox("Select Source Node", nodes)
target = st.sidebar.selectbox("Select Target Node", nodes)

# Calculate resilient path
path = resilient_path(G, source, target)

# Display results
if path:
    st.success(f"Resilient Path from {source} to {target}: {path}")
else:
    st.error("No resilient path available between selected nodes.")

# Graph visualization
pos = nx.spring_layout(G, seed=42)
plt.figure(figsize=(6, 5))
nx.draw(G, pos, with_labels=True, node_size=2000, node_color="lightblue", font_size=12, font_weight="bold")
labels = nx.get_edge_attributes(G, "weight")
nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
st.pyplot(plt)
