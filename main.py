# main.py
from graph_data import nodes, edges, positions, categories
from dijkstra import build_graph, dijkstra, reconstruct_path
from plotting import plot_graph_and_path



def print_menu():
    print("=== 台科大校園最短路徑查詢系統 ===")
    for i, name in enumerate(nodes):
        print(f"{i:2d}. {name}")
    print()


def main():
    graph = build_graph(nodes, edges)

    while True:
        print_menu()

        try:
            start_idx = int(input("請輸入起點編號（-1 結束）："))
            if start_idx == -1:
                print("程式結束，再見！")
                break
            end_idx = int(input("請輸入終點編號："))
        except ValueError:
            print("請輸入整數。\n")
            continue

        if not (0 <= start_idx < len(nodes) and 0 <= end_idx < len(nodes)):
            print("編號範圍錯誤。\n")
            continue

        start = nodes[start_idx]
        end = nodes[end_idx]

        dist, prev = dijkstra(graph, start)
        path = reconstruct_path(prev, start, end)

        if not path:
            print(f"從 {start} 到 {end} 無路徑\n")
            continue

        print("\n=== 最短路徑結果 ===")
        print("起點：", start)
        print("終點：", end)
        print("路徑：", " → ".join(path))
        print("總距離：", dist[end], "m\n")

        show = input("顯示地圖結果？(y/n)：").lower()
        if show == 'y':
            plot_graph_and_path(nodes, edges, positions, path)


if __name__ == "__main__":
    main()
