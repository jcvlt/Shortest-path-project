# plotting.py
import matplotlib.pyplot as plt
from graph_data import categories


color_map = {
    "gate": "black",
    "admin": "blue",
    "public": "gold",
    "teaching": "green",
    "research": "purple",
    "sport": "red",
    "dorm": "orange",
    "cafeteria": "pink"
}


def plot_graph_and_path(nodes, edges, positions, path):
    plt.figure(figsize=(8, 8))

    # 所有邊
    for u, v, w in edges:
        x1, y1 = positions[u]
        x2, y2 = positions[v]
        plt.plot([x1, x2], [y1, y2], linestyle='-', linewidth=1)

    # 節點
    xs = [positions[name][0] for name in nodes]
    ys = [positions[name][1] for name in nodes]
    # 用分類給節點上色
    colors = [color_map[categories[name]] for name in nodes]
    plt.scatter(xs, ys, c=colors, s=80, edgecolors='black', linewidths=0.5)


    # 名稱
    for name in nodes:
        x, y = positions[name]
        plt.text(x + 0.05, y + 0.05, name, fontsize=8)

    # 最短路徑上色
    if path and len(path) > 1:
        for i in range(len(path) - 1):
            u = path[i]
            v = path[i + 1]
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            plt.plot([x1, x2], [y1, y2],
                     linestyle='-', linewidth=3, color='red')

    plt.title("Taiwan Tech Campus Shortest Path")
    plt.axis('off')
    plt.tight_layout()
    # 圖例
    for category, color in color_map.items():
        plt.scatter([], [], c=color, label=category, s=80, edgecolors='black')

    plt.legend(title="Node Categories", loc="upper left", bbox_to_anchor=(1,1))
    plt.show()