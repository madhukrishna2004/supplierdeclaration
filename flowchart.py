import matplotlib.pyplot as plt
import networkx as nx

# Create a directed graph to represent the flowchart
G = nx.DiGraph()

# Add nodes representing the stages in the flowchart
nodes = [
    ("Login Page", "Enter credentials (username & password)\nOption for password recovery/account creation"),
    ("Dashboard", "Search bar, commodity list,\nreal-time tariff updates, quick access features"),
    ("Commodity Search", "Search by HS code or description\nDisplay of commodity info (HS code, tariff rate, VAT, origin)"),
    ("Bill of Materials (BOM)", "Upload BOM for automated origin detection\nDisplay tariff codes and product origin"),
    ("Tariff Updates", "Receive real-time updates\nNotifications about tariff changes and regulatory updates"),
    ("Reports & Analytics", "Generate and download reports (CSV, PDF, Excel)"),
    ("User Profile & Settings", "Manage details, subscription plans, notifications"),
    ("Help/Support", "FAQs, tutorial guides, customer support contact")
]

# Add edges to represent the flow between nodes
edges = [
    ("Login Page", "Dashboard"),
    ("Dashboard", "Commodity Search"),
    ("Commodity Search", "Bill of Materials (BOM)"),
    ("Bill of Materials (BOM)", "Tariff Updates"),
    ("Tariff Updates", "Reports & Analytics"),
    ("Reports & Analytics", "User Profile & Settings"),
    ("User Profile & Settings", "Help/Support")
]

# Add nodes and edges to the graph
G.add_nodes_from([node[0] for node in nodes])
G.add_edges_from(edges)

# Position nodes using a spring layout
pos = nx.spring_layout(G, seed=42)

# Create the figure
plt.figure(figsize=(12, 8))

# Draw the graph
nx.draw(G, pos, with_labels=True, node_size=4000, node_color='lightblue', font_size=10, font_weight='bold', arrows=True, edge_color='gray')

# Annotate the nodes with the descriptions
for i, node in enumerate(nodes):
    x, y = pos[node[0]]
    plt.text(x, y - 0.1, node[1], horizontalalignment='center', verticalalignment='center', fontweight='light', fontsize=8, color='black')

# Title for the flowchart
plt.title("Tradesphere Global Flowchart", fontsize=16, fontweight='bold')

# Save the plot as a PNG file
plt.axis('off')
plt.savefig("tradesphere_flowchart.png", format="PNG")

# Show the plot
plt.show()
