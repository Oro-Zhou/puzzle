import networkx as nx
import matplotlib.pyplot as plt

def generate_graph(index_dict={"R":(0,0),"B":(0,1),"G":(1,0),"Y":(1,1),"P":(2,0)}):
    #依照index_dict製圖
    G = nx.Graph()  

    Color_list = ['red', 'blue', 'green', "yellow","purple"]
    category_list = ['R', 'B', 'G', "Y", "P"]
    direction_list = [1, 2, 3, 4, 5, 6]  # 這裡是數字，需要轉換成字串來拼接

    for category in range(len(category_list)):
        for direction in range(len(direction_list)):
            name = category_list[category] + str(direction_list[direction])  # 轉換 direction 為字串
            G.add_node(name, 
                    category=category_list[category], 
                    description=direction_list[direction], 
                    color=Color_list[category],
                    label="")
            
    #這裡未來要決定各點的label
    G.nodes["R1"]["label"]='Door'
    G.nodes["G3"]["label"]='Key'
    G.nodes["Y2"]["label"]='R'
    G.nodes["B4"]["label"]='G'

    #這裡未來要決定各版塊內部連接
    G.add_edges_from([("R1", "R3"), ("R2", "R4")])
    G.add_edges_from([("B1", "B4"), ("B2", "B3")])
    G.add_edges_from([("G1", "G3")])
    G.add_edges_from([("Y1", "Y2"),("Y4", "Y2"),("Y1", "Y4")])

    keylist = list(index_dict.keys())
    valuelist = list(index_dict.values())

    for i in range(len(index_dict)):
        for j in range(i+1,len(index_dict)):
            x_1,y_1 = valuelist[i]
            x_2,y_2 = valuelist[j]
            if x_1-x_2==0 and y_1-y_2==-1:
                G.add_edge(keylist[i]+"1",keylist[j]+"4")
            elif x_1-x_2==1 and y_1-y_2==-1:
                G.add_edge(keylist[i]+"2",keylist[j]+"5")
            elif x_1-x_2==1 and y_1-y_2==0:
                G.add_edge(keylist[i]+"3",keylist[j]+"6")
            elif x_1-x_2==0 and y_1-y_2==1:
                G.add_edge(keylist[i]+"4",keylist[j]+"1")
            elif x_1-x_2==-1 and y_1-y_2==1:
                G.add_edge(keylist[i]+"5",keylist[j]+"2")
            elif x_1-x_2==-1 and y_1-y_2==0:
                G.add_edge(keylist[i]+"6",keylist[j]+"3")
    return G


def plot_graph(G):
    # 繪製圖形
    node_colors = [G.nodes[node]['color'] for node in G.nodes()]
    labels = {node: G.nodes[node].get("label", "") for node in G.nodes()}
    pos = nx.spring_layout(G, seed=42)  # 讓節點排列更整齊
    plt.figure(figsize=(6, 6))
    nx.draw(G, pos, with_labels=True, node_color=node_colors, edge_color="gray", node_size=300, font_size=10)
    pos_shifted = {node: (x, y + 0.07) for node, (x, y) in pos.items()}  # label 上移
    # 顯示主要標籤（label）
    nx.draw_networkx_labels(G, pos_shifted, labels, font_size=12, font_color="black")
    plt.show()


def node_connected_label(G,Node):
# 查詢 Node 所有連通的label
    labellist={}
    connected_nodes = list(nx.node_connected_component(G, Node))
    for name in connected_nodes:
        node=G.nodes[name]
        if node["label"] != "":
            labellist[name]=node["label"]
    return labellist


def Legal_movement(index_dict, plate):
    #在index_dict中plate可移動位置
    new_index_set = set()  
    adj_list = [(0,1), (1,0), (-1,0), (0,-1), (-1,1), (1,-1)]
    occupied_positions = set(index_dict.values())  # 轉為 set 加速查找
    for key, (x1, y1) in index_dict.items():
        if key == plate:
            continue  # 跳過 plate 這個 key
        for dx, dy in adj_list:
            new_pos = (x1 + dx, y1 + dy)
            if new_pos not in occupied_positions and new_pos not in new_index_set:
                new_index_set.add(new_pos)
    return list(new_index_set) 


index_dict={"R":(0,0),"B":(0,1),"G":(1,0),"Y":(1,1),"P":(2,0)}

G = generate_graph(index_dict)
plot_graph(G)
labellist=node_connected_label(G, "R1")
print(labellist)
move_index=Legal_movement(index_dict,"R")
print(move_index)
