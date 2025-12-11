import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

from graph_data import nodes, edges, positions, categories
from dijkstra import build_graph, dijkstra, reconstruct_path
from plotting import color_map

class CampusNavApp:
    def __init__(self, root):
        self.root = root
        self.root.title("台科大校園最短路徑導航系統")
        self.root.geometry("1000x700")

        self.graph = build_graph(nodes, edges)

        # ------------Layout
        
        # left panel
        control_frame = ttk.Frame(root, padding="20")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # title
        ttk.Label(control_frame, text="導航設定", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # start point menu
        ttk.Label(control_frame, text="請選擇起點:").pack(anchor="w")
        self.start_combo = ttk.Combobox(control_frame, values=nodes, state="readonly")
        self.start_combo.pack(fill=tk.X, pady=(0, 15))
        self.start_combo.current(0) #choose first as default

        # end point menu
        ttk.Label(control_frame, text="請選擇終點:").pack(anchor="w")
        self.end_combo = ttk.Combobox(control_frame, values=nodes, state="readonly")
        self.end_combo.pack(fill=tk.X, pady=(0, 15))
        self.end_combo.current(1) # choose second as default

        # calculate button
        self.calc_btn = ttk.Button(control_frame, text="計算最短路徑", command=self.on_calculate)
        self.calc_btn.pack(fill=tk.X, pady=10)

        # print result output
        ttk.Label(control_frame, text="路徑詳情:", font=("Arial", 12, "bold")).pack(pady=(20, 5), anchor="w")
        self.result_text = tk.Text(control_frame, height=15, width=30, state="disabled", bg="#f0f0f0")
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # left panel (map)
        map_frame = ttk.Frame(root)
        map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=map_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.draw_map(path=[])

    def on_calculate(self):
        start_node = self.start_combo.get()
        end_node = self.end_combo.get()

        if start_node == end_node:
            messagebox.showwarning("提示", "起點與終點相同！")
            return

        dist_map, prev_map = dijkstra(self.graph, start_node)
        path = reconstruct_path(prev_map, start_node, end_node)

        self.update_result_text(start_node, end_node, path, dist_map[end_node])
        
        self.draw_map(path)

    def update_result_text(self, start, end, path, total_dist):
        self.result_text.config(state="normal")
        self.result_text.delete(1.0, tk.END)
        
        if not path:
            self.result_text.insert(tk.END, f"無法從 {start} 到達 {end}\n")
        else:
            self.result_text.insert(tk.END, f"起點: {start}\n")
            self.result_text.insert(tk.END, f"終點: {end}\n")
            self.result_text.insert(tk.END, f"總距離: {total_dist} m\n\n")
            self.result_text.insert(tk.END, "路徑順序:\n")
            for i, node in enumerate(path):
                if i == 0: prefix = ""
                else: prefix = " ⭢ "
                self.result_text.insert(tk.END, f"{prefix}{node}")
        
        self.result_text.config(state="disabled")

    def draw_map(self, path):
        self.ax.clear()

        # draw all paths
        for u, v, w in edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            self.ax.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=1, alpha=0.5)

        # draw nodes
        for name in nodes:
            x, y = positions[name]
            color = color_map.get(categories.get(name), 'gray')
            self.ax.scatter(x, y, c=color, s=100, edgecolors='black', zorder=5)
            # label
            self.ax.text(x + 0.1, y + 0.1, name, fontsize=9)

        # highlight path
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                x1, y1 = positions[u]
                x2, y2 = positions[v]
                self.ax.plot([x1, x2], [y1, y2], color='red', linestyle='-', linewidth=3, zorder=4)

        self.ax.set_title("Taiwan Tech Campus Map")
        self.ax.axis('off')
        
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    app = CampusNavApp(root)

    root.mainloop()
