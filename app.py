import customtkinter as ctk
from tkinter import messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.patches import Rectangle

from graph_data import nodes, edges, positions, categories, edge_waypoints, node_dims, color_map
from dijkstra import build_graph, dijkstra, reconstruct_path

ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

class CampusPathFinder(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Navigation System")
        self.geometry("1100x750")
        
        self.graph = build_graph(nodes, edges) # initialize graph

        visible_nodes = [n for n in nodes if not n.startswith("N")]

        # grid layout
        self.grid_columnconfigure(1, weight=1) # set col 1 resizable
        self.grid_rowconfigure(0, weight=1) # set row 0 resizable

        # side bar
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsew")
        
        # title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame,
                                       text="NTUST Navigation",
                                       font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.pack(padx=20, pady=(20, 10))

        # start point 
        self.label_start = ctk.CTkLabel(self.sidebar_frame, text="From:")
        self.label_start.pack(padx=20, pady=(10, 0))

        self.start_combo = ctk.CTkComboBox(self.sidebar_frame, values=visible_nodes)
        self.start_combo.pack(padx=20, pady=5)
        self.start_combo.set(visible_nodes[0]) #default choose first

        # End point 
        self.label_end = ctk.CTkLabel(self.sidebar_frame, text="To:")
        self.label_end.pack(padx=20, pady=(10, 0))
        
        self.end_combo = ctk.CTkComboBox(self.sidebar_frame, values=visible_nodes)
        self.end_combo.pack(padx=20, pady=5)
        self.end_combo.set(visible_nodes[1]) #default choose second

        # calculate btn
        self.calc_btn = ctk.CTkButton(self.sidebar_frame, text="Go!", 
                                    command=self.calculate,
                                    font=ctk.CTkFont(size=15, weight="bold"),
                                    height=40,
                                    corner_radius=20)
        self.calc_btn.pack(padx=20, pady=30)

        # output textbox
        self.result_label = ctk.CTkLabel(self.sidebar_frame, text="Navigation Details:", anchor="w")
        self.result_label.pack(padx=20, pady=(10, 0), fill="x")
        
        self.result_text = ctk.CTkTextbox(self.sidebar_frame, height=200)
        self.result_text.pack(padx=20, pady=(5, 20), fill="both", expand=True)
        self.result_text.configure(state="disabled")

        # map section
        self.map_frame = ctk.CTkFrame(self, corner_radius=10)
        self.map_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")

        # matplotlib diagram
        self.fig = Figure(figsize=(6, 6), dpi=100, facecolor='#2b2b2b')
        self.ax = self.fig.add_subplot(111)
        self.ax.set_facecolor('#2b2b2b')
        
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.map_frame)
        self.canvas.get_tk_widget().pack(side="top", fill="both", expand=True, padx=10, pady=10)

        self.draw_map(path=[])

    def calculate(self):
        start_node = self.start_combo.get()
        end_node = self.end_combo.get()

        if start_node == end_node:
            messagebox.showwarning("Warning", "Start point and end point cannot be the same.")
            return

        dist_map, prev_map = dijkstra(self.graph, start_node)
        path = reconstruct_path(prev_map, start_node, end_node)

        self.update_result_text(start_node, end_node, path, dist_map[end_node])
        self.draw_map(path)

    def update_result_text(self, start, end, path, total_dist):
        self.result_text.configure(state="normal")
        self.result_text.delete("1.0", "end")
        
        if not path:
            self.result_text.insert("end", f"No path from {start} to {end}\n")
        else:
            output_text = f"Start: {start}\nDestination: {end}\nDistance: {total_dist} m\n\n"
            self.result_text.insert("end", output_text)

        self.result_text.configure(state="disabled")

    def draw_map(self, path):
        self.ax.clear()

        # draw lines
        def get_plot_points(u, v): # get start/end point
            start_pos = positions[u]
            end_pos = positions[v]
            key = tuple(sorted((u, v)))

            if key in edge_waypoints: # has waypoints
                waypoints = edge_waypoints[key]
                if u == key[1]: waypoints = waypoints[::-1] # reverse if needed
                return [start_pos] + waypoints + [end_pos]
            return [start_pos, end_pos]

        for u, v, w in edges:
            points = get_plot_points(u, v)
            xs = [p[0] for p in points]
            ys = [p[1] for p in points]
            self.ax.plot(xs, ys, color='#FFFFFF', linestyle='-', linewidth=1, alpha=0.5)

        # draw rectangles
        for name in nodes:
            if name.startswith("N"): # skip invisible nodes
                continue

            cx, cy = positions[name]  # center x,y
            
            w, h = node_dims.get(name, (1, 1)) #if not set, default is (1,1)
            
            # 左下角 coordinate bc Matplotlib starts to draw from 左下角
            left = cx - (w / 2)
            bottom = cy - (h / 2)
            
            c = color_map.get(categories.get(name), 'gray') #if not set, default is gray
            
            rect = Rectangle(
                (left, bottom), width=w, height=h,
                facecolor=c,
                edgecolor='white',
                linewidth=1,
                zorder=5
            )
            self.ax.add_patch(rect)

            # label
            self.ax.text(cx, cy, name, 
                         fontsize=12, color='white', fontweight='bold',
                         ha='center', va='center', zorder=6)

        # draw the shrotest path
        if path and len(path) > 1:
            for i in range(len(path) - 1):
                u = path[i]
                v = path[i + 1]
                points = get_plot_points(u, v)
                px = [p[0] for p in points]
                py = [p[1] for p in points]
                self.ax.plot(px, py, color='#FF0000', linestyle='-', linewidth=4, alpha=0.8, zorder=4)

        self.ax.set_title("Campus Map", fontsize=24, color='white', pad=20)
        self.ax.axis('off')
        
        self.ax.set_aspect('equal') # ratio 1:1
        self.ax.autoscale_view()
        
        self.canvas.draw()
    

if __name__ == "__main__":
    app = CampusPathFinder()
    app.mainloop()
