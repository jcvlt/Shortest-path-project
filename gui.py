import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 匯入你原本的模組
from graph_data import nodes, edges, positions, categories
from dijkstra import build_graph, dijkstra, reconstruct_path
from plotting import color_map # 重用原本定義的顏色

class CampusNavApp:
    def __init__(self, root):
        self.root = root
        self.root.title("台科大校園最短路徑導航系統")
        self.root.geometry("1000x700")

        # 初始化圖形資料
        self.graph = build_graph(nodes, edges)

        # --- 建立介面配置 (Layout) ---
        
        # 1. 左側控制面板
        control_frame = ttk.Frame(root, padding="20")
        control_frame.pack(side=tk.LEFT, fill=tk.Y)

        # 標題
        ttk.Label(control_frame, text="導航設定", font=("Arial", 16, "bold")).pack(pady=(0, 20))

        # 起點選單
        ttk.Label(control_frame, text="請選擇起點:").pack(anchor="w")
        self.start_combo = ttk.Combobox(control_frame, values=nodes, state="readonly")
        self.start_combo.pack(fill=tk.X, pady=(0, 15))
        self.start_combo.current(0) # 預設選第一個

        # 終點選單
        ttk.Label(control_frame, text="請選擇終點:").pack(anchor="w")
        self.end_combo = ttk.Combobox(control_frame, values=nodes, state="readonly")
        self.end_combo.pack(fill=tk.X, pady=(0, 15))
        self.end_combo.current(1) # 預設選第二個

        # 計算按鈕
        self.calc_btn = ttk.Button(control_frame, text="計算最短路徑", command=self.on_calculate)
        self.calc_btn.pack(fill=tk.X, pady=10)

        # 結果顯示區 (文字)
        ttk.Label(control_frame, text="路徑詳情:", font=("Arial", 12, "bold")).pack(pady=(20, 5), anchor="w")
        self.result_text = tk.Text(control_frame, height=15, width=30, state="disabled", bg="#f0f0f0")
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 2. 右側地圖顯示區
        map_frame = ttk.Frame(root)
        map_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 初始化 Matplotlib 圖表 (嵌入式)
        self.fig = Figure(figsize=(6, 6), dpi=100)
        self.ax = self.fig.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.fig, master=map_frame)
        self.canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # 繪製初始地圖 (無路徑)
        self.draw_map(path=[])

    def on_calculate(self):
        start_node = self.start_combo.get()
        end_node = self.end_combo.get()

        if start_node == end_node:
            messagebox.showwarning("提示", "起點與終點相同！")
            return

        # 執行 Dijkstra 演算法
        dist_map, prev_map = dijkstra(self.graph, start_node)
        path = reconstruct_path(prev_map, start_node, end_node)

        # 顯示結果文字
        self.update_result_text(start_node, end_node, path, dist_map[end_node])
        
        # 更新地圖
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
                # prefix = "└─ " if i == len(path)-1 else "├─ "
                if i == 0: prefix = ""
                else: prefix = " ⭢ "
                self.result_text.insert(tk.END, f"{prefix}{node}")
        
        self.result_text.config(state="disabled")

    def draw_map(self, path):
        # 清除舊圖
        self.ax.clear()

        # 1. 繪製所有邊 (灰色背景線)
        for u, v, w in edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            self.ax.plot([x1, x2], [y1, y2], color='gray', linestyle='-', linewidth=1, alpha=0.5)

        # 2. 繪製節點
        for name in nodes:
            x, y = positions[name]
            color = color_map.get(categories.get(name), 'gray')
            self.ax.scatter(x, y, c=color, s=100, edgecolors='black', zorder=5)
            # 節點名稱
            self.ax.text(x + 0.1, y + 0.1, name, fontsize=9)

        # 3. 如果有路徑，繪製紅色高亮線
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                x1, y1 = positions[u]
                x2, y2 = positions[v]
                self.ax.plot([x1, x2], [y1, y2], color='red', linestyle='-', linewidth=3, zorder=4)

        self.ax.set_title("Taiwan Tech Campus Map")
        self.ax.axis('off') # 隱藏座標軸
        
        # 刷新畫布
        self.canvas.draw()

if __name__ == "__main__":
    root = tk.Tk()
    # 設定視窗圖示 (可選)
    # root.iconbitmap('icon.ico') 
    app = CampusNavApp(root)
    root.mainloop()