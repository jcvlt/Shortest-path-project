# main.py
from graph_data import nodes, edges, positions, categories
from dijkstra import build_graph, dijkstra, reconstruct_path
from plotting import plot_graph_and_path



def print_menu():
    print("=== NTUST Campus Shortest Path Finder ===")
    for i, name in enumerate(nodes):
        print(f"{i:2d}. {name}")
    print()


def main():
    graph = build_graph(nodes, edges)

    while True:
        print_menu()

        try:
            start_idx = int(input("Enter the start point（-1 to exit）："))
            if start_idx == -1:
                print("Program finished.")
                break
            end_idx = int(input("Enter the destination point："))
        except ValueError:
            print("Please enter an integer value.\n")
            continue

        if not (0 <= start_idx < len(nodes) and 0 <= end_idx < len(nodes)):
            print("Invalid number.\n")
            continue

        start = nodes[start_idx]
        end = nodes[end_idx]

        dist, prev = dijkstra(graph, start)
        path = reconstruct_path(prev, start, end)

        if not path:
            print(f"No path from {start} to {end}.\n")
            continue

        print("\n=== Shortest Path ===")
        print("Start：", start)
        print("Destination：", end)
        print("Path：", " → ".join(path))
        print("Distance：", dist[end], "m\n")

        show = input("Show map？(y/n)：").lower()
        if show == 'y':
            plot_graph_and_path(nodes, edges, positions, path)


if __name__ == "__main__":
    main()

