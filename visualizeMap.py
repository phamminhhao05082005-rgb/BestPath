import matplotlib.pyplot as plt
import networkx as nx
from roads import road_names

def visualize_map(map_data, path=None):
    # Tạo graph có hướng hoặc vô hướng
    G = nx.DiGraph() if map_data.directed else nx.Graph()

    # Thêm các cạnh
    for (u, v), dist in map_data.distance_km.items():
        G.add_edge(u, v, weight=dist)

    # Vị trí node
    pos = {node: (coord[0], coord[1]) for node, coord in map_data.locations.items()}

    plt.figure(figsize=(20, 16))
    ax = plt.gca()

    # Vẽ cạnh mặc định
    nx.draw_networkx_edges(G, pos, edge_color="gray", arrows=map_data.directed, width=2)

    # Các node bình thường (không thuộc path)
    normal_nodes = list(G.nodes()) if not path else [n for n in G.nodes() if n not in path]
    nx.draw_networkx_nodes(G, pos, nodelist=normal_nodes, node_size=1200, node_color="lightgreen")
    nx.draw_networkx_labels(G, pos, labels={n: n for n in normal_nodes}, font_size=20,
                            font_color="black", font_weight="bold")

    # Nếu có đường đi
    if path:
        path_edges = list(zip(path, path[1:]))
        nx.draw_networkx_edges(G, pos, edgelist=path_edges, edge_color="blue", width=4)

        # Node đầu (đen)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[0]], node_size=1500, node_color="black")
        nx.draw_networkx_labels(G, pos, labels={path[0]: path[0]}, font_size=20,
                                font_color="white", font_weight="bold")

        # Node đích (xanh dương)
        nx.draw_networkx_nodes(G, pos, nodelist=[path[-1]], node_size=1500, node_color="red")
        nx.draw_networkx_labels(G, pos, labels={path[-1]: path[-1]}, font_size=20,
                                font_color="white", font_weight="bold")

        # Node trung gian (vàng)
        middle_nodes = path[1:-1] if len(path) > 2 else []
        if middle_nodes:
            nx.draw_networkx_nodes(G, pos, nodelist=middle_nodes, node_size=1400, node_color="gold")
            nx.draw_networkx_labels(G, pos, labels={n: n for n in middle_nodes}, font_size=20,
                                    font_color="red", font_weight="bold")

    # Hiển thị tên đường
    edge_labels = {}
    for u, v in G.edges():
        road_label = road_names.get((u, v)) or road_names.get((v, u)) or "???"
        edge_labels[(u, v)] = road_label
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=12,
                                 font_color="purple", font_weight="bold")

    plt.axis("off")

    # Toàn màn hình (tùy môi trường)
    manager = plt.get_current_fig_manager()
    try:
        manager.full_screen_toggle()
    except AttributeError:
        manager.window.showMaximized()

    plt.tight_layout()
    plt.show()
