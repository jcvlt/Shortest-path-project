# graph_data.py
# 台科大校園節點、邊、座標資料

nodes = [
    "MainGate", "AD", "IB", "T1", "T2", "T3", "T4",
    "E1", "E2", "EE", "MA", "S", "Library", "Gym",
    "Court", "IA", "Dorm1", "Dorm2", "Dorm3", "RB",
    "TR", "Caf1", "Caf3"
]

edges = [
    ("MainGate", "AD", 100),
    ("MainGate", "IB", 180.28),
    ("MainGate", "Library", 180.28),
    ("AD", "IB", 150),
    ("AD", "Dorm2", 300),
    ("AD", "Dorm3", 316.23),
    ("AD", "E1", 250),
    ("AD", "Library", 150),
    ("IB", "E2", 150),
    ("Library", "T1", 100),
    ("Library", "T4", 70.71),
    ("Library", "RB", 70.71),
    ("RB", "T1", 70.71),
    ("RB", "T4", 100),
    ("T1", "T4", 70.71),
    ("T4", "Caf1", 223.61),
    ("E1", "Caf1", 200),
    ("E1", "T3", 180.28),
    ("E1", "Dorm1", 150),
    ("Caf3", "E2", 50),
    ("Caf3", "T2", 50),
    ("Caf3", "EE", 100),
    ("Caf3", "MA", 50),
    ("EE", "Dorm2", 150),
    ("EE", "MA", 111.8),
    ("EE", "T2", 111.8),
    ("E2", "MA", 70.71),
    ("E2", "T2", 70.71),
    ("Dorm2", "Dorm3", 100),
    ("Dorm1", "Dorm3", 100),
    ("Dorm1", "T3", 158.11),
    ("S", "T3", 70.71),
    ("S", "Caf1", 50),
    ("S", "Gym", 100),
    ("S", "IA", 206.16),
    ("Gym", "IA", 158.11),
    ("Gym", "Caf1", 158.11),
    ("TR", "IA", 150),
    ("TR", "Court", 100),
    ("T1", "Court", 250),
]

positions = {
    "MainGate": (0, 0),
    "AD": (0, 0.5),
    "RB": (-2, 0.25),
    "Library": (-1.5, 0.5),
    "T1": (-2.5, 0.5),
    "T4": (-2, 0.75),
    "T2": (2, 1.5),
    "T3": (-3.5, 1.75),
    "TR": (-6, 0.5),
    "EE": (1.5, 2),
    "MA": (1, 1.5),
    "IB": (1.5, 0.5),
    "S": (-4, 1.5),
    "Gym": (-5, 1.5),
    "Court": (-5, 0.5),
    "IA": (-6, 1.25),
    "E1": (-2, 1.25),
    "E2": (1.5, 1.25),
    "Dorm1": (-2, 2),
    "Dorm2": (0, 2),
    "Dorm3": (-1, 2),
    "Caf1": (-4, 1.25),
    "Caf3": (1.5, 1.5)
}

# 建築分類
categories = {
    "MainGate": "gate",

    # 行政與公共
    "AD": "admin",
    "Library": "public",
    "S": "public",

    # 教學大樓
    "IB": "teaching",
    "T1": "teaching",
    "T2": "teaching",
    "T3": "teaching",
    "T4": "teaching",
    "E1": "teaching",
    "E2": "teaching",
    "EE": "teaching",
    "MA": "teaching",

    # 研究大樓
    "RB": "research",
    "TR": "research",
    "IA": "research",

    # 運動區
    "Gym": "sport",
    "Court": "sport",

    # 宿舍
    "Dorm1": "dorm",
    "Dorm2": "dorm",
    "Dorm3": "dorm",

    # 餐廳
    "Caf1": "cafeteria",
    "Caf3": "cafeteria",
}
