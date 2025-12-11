import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

# 匯入原本的邏輯與資料
from graph_data import nodes, edges, positions, categories
from dijkstra import build_graph, dijkstra, reconstruct_path
from plotting import color_map

# --- 設定全域主題 ---
ctk.set_appearance_mode("Dark")  # 模式: "System" (標準), "Dark", "Light"
ctk.set_default_color_theme("blue")  # 主題顏色: "blue", "green", "dark-blue"

class ModernCampusNav(ctk.CTk):
    def __init__(self):
        super().__init__()

        # 1. 視窗基礎設定
        self.title("台科大校園導航系統 (Modern UI)")
        self.geometry("1100x750")
        
        # 初始化圖形資料
        self.graph = build_graph(nodes, edges)

        # 2. 建立主要佈局 (Grid Layout)
        self.grid_columnconfigure(1, weight=1) # 右邊地圖區會隨視窗縮放
        self.grid_rowconfigure(0, weight=1)

        # --- 左側控制面板 (Sidebar) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # 標題
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="NTUST Navigation", 
                                     font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        # 起點選單
        self.label_start = ctk.CTkLabel(self.sidebar_frame, text="選擇起點:", anchor="w")
        self.label_start.pack(padx=20, pady=(10, 0), fill="x")
        self.start_combo = ctk.CTkComboBox(self.sidebar_frame, values=nodes)
        self.start_combo.pack(padx=20, pady=5)
        self.start_combo.set(nodes[0]) # 預設值

        # 終點選單
        self.label_end = ctk.CTkLabel(self.sidebar_frame, text="選擇終點:", anchor="w")
        self.label_end.pack(padx=20, pady=(10, 0), fill="x")
        self.end_combo = ctk.CTkComboBox(self.sidebar_frame, values=nodes)
        self.end_combo.pack(padx=20, pady=5)
        self.end_combo.set(nodes[1]) # 預設值

        # 計算按鈕 (加大、更顯眼)
        self.calc_btn = ctk.CTkButton(self.sidebar_frame, text="開始導航", 
                                    command=self.on_calculate,
                                    font=ctk.CTkFont(size=15, weight="bold"),
                                    height=40)
        self.calc_btn.pack(padx=20, pady=30)

        # 結果顯示區 (Textbox)
        self.result_label = ctk.CTkLabel(self.sidebar_frame, text="導航資訊:", anchor="w")
        self.result_label.pack(padx=20, pady=(10, 0), fill="x")
        
        self.result_text = ctk.CTkTextbox(self.sidebar_frame, height=200)
        self.result_text.pack(padx=20, pady=(5, 20), fill="both", expand=True)
        self.result_text.configure(state="disabled") # 唯讀模式

        # --- 右側地圖顯示區 ---
        self.map_frame = ctk.CTkFrame(self, corner_radius=10)
        self.map_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # 嵌入 Matplotlib 圖表
        # 設定圖表背景色以配合 Dark Mode (接近 #2b2b2b)
        self.fig = Figure(figsize=(6, 6), dpi=100, facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b2b2b') # 座標軸背景也設為深色
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

        # 初始繪圖
        self.draw_map(path=[])

    def on_calculate(self):
        start_node = self.start_combo.get()
        end_node = self.end_combo.get()

        if start_node == end_node:
            # CustomTkinter 沒有內建 messagebox，通常混用 tkinter 的
            messagebox.showwarning("提示", "起點與終點不能相同！")
            return

        dist_map, prev_map = dijkstra(self.graph, start_node)
        path = reconstruct_path(prev_map, start_node, end_node)

        self.update_result_text(start_node, end_node, path, dist_map[end_node])
        self.draw_map(path)

    def update_result_text(self, start, end, path, total_dist):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        
        if not path:
            self.result_text.insert("end", f"無路徑連結 {start} 與 {end}\n")
        else:
            header = f"起點: {start}\n終點: {end}\n距離: {total_dist} m\n\n"
            self.result_text.insert("end", header)
            self.result_text.insert("end", "路徑規劃:\n")
            for i, node in enumerate(path):
                if i == 0:
                    self.result_text.insert("end", f"● {node}\n")
                elif i == len(path) - 1:
                    self.result_text.insert("end", f"★ {node}\n")
                else:
                    self.result_text.insert("end", f"↓ {node}\n")
        
        self.result_text.configure(state="disabled")

    def draw_map(self, path):
        self.ax.clear()
        
        # 1. 繪製連線 (更淡的顏色以適應深色背景)
        for u, v, w in edges:
            x1, y1 = positions[u]
            x2, y2 = positions[v]
            self.ax.plot([x1, x2], [y1, y2], color='#555555', linestyle='-', linewidth=1, alpha=0.6)

        # 2. 繪製節點
        for name in nodes:
            x, y = positions[name]
            c = color_map.get(categories.get(name), 'gray')
            self.ax.scatter(x, y, c=c, s=120, edgecolors='white', linewidths=0.8, zorder=5)
            # 文字改為白色，並稍微加粗
            self.ax.text(x + 0.1, y + 0.1, name, fontsize=9, color='white', fontweight='bold')

        # 3. 繪製最短路徑 (亮青色 Cyan 或 螢光紅，在深色底比較顯眼)
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                x1, y1 = positions[u]
                x2, y2 = positions[v]
                # 使用螢光色系
                self.ax.plot([x1, x2], [y1, y2], color='#00ffcc', linestyle='-', linewidth=4, alpha=0.8, zorder=4)

        self.ax.set_title("Campus Map", color='white', pad=20)
        self.ax.axis('off') # 關閉座標軸
        self.canvas.draw()

if __name__ == "__main__":
    app = ModernCampusNav()
    app.mainloop()