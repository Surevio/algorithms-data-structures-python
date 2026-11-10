import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import random

# Функция для поиска достижимых вершин
def find_reachable_nodes(graph, start_node):
    reachable_nodes = set()
    stack = [start_node]
    
    while stack:
        node = stack.pop()
        if node not in reachable_nodes:
            reachable_nodes.add(node)
            neighbors = list(graph.neighbors(node))
            stack.extend(neighbors)
    
    return reachable_nodes

# Функция для отображения результата поиска в отдельном окне
def show_result_graph(graph, reachable_nodes, start_node):
    result_window = tk.Toplevel(root)
    result_window.title("Результат поиска")

    fig, ax = plt.subplots(figsize=(6, 4))
    pos = nx.spring_layout(graph)  # Определяем расположение вершин
    
    # Рисуем все вершины
    nx.draw_networkx_nodes(graph, pos, node_size=500, node_color="lightblue", ax=ax)
    
    # Выделяем достижимые вершины
    nx.draw_networkx_nodes(graph, pos, nodelist=reachable_nodes, node_color="yellow", ax=ax)
    
    # Выделяем начальную вершину
    nx.draw_networkx_nodes(graph, pos, nodelist=[start_node], node_color="red", ax=ax)
    
    # Рисуем ребра
    nx.draw_networkx_edges(graph, pos, arrowstyle="->", arrowsize=20, ax=ax)
    
    # Подписываем вершины
    nx.draw_networkx_labels(graph, pos, ax=ax)
    
    ax.set_title("Результат поиска достижимых вершин")
    
    # Встраиваем график в окно
    canvas = FigureCanvasTkAgg(fig, master=result_window)
    canvas.get_tk_widget().pack(fill=tk.BOTH, expand=1)
    canvas.draw()

# Функция для обработки нажатия кнопки в графическом интерфейсе
def on_button_click():
    try:
        start_node = int(entry.get())
        if start_node not in G.nodes:
            messagebox.showerror("Ошибка", f"Вершина {start_node} отсутствует в графе.")
            return
        
        reachable_nodes = find_reachable_nodes(G, start_node)
        messagebox.showinfo("Результат", f"Достижимые вершины из {start_node}: {reachable_nodes}")
        show_result_graph(G, reachable_nodes, start_node)
    except ValueError:
        messagebox.showerror("Ошибка", "Пожалуйста, введите целое число.")

# Функция для генерации случайного графа
def generate_random_graph():
    num_nodes = random.randint(5, 10)  # Случайное количество вершин (от 5 до 10)
    probability = 0.3  # Вероятность наличия ребра между вершинами
    G = nx.gnp_random_graph(num_nodes, probability, directed=True)
    return G

# Создаем случайный граф
G = generate_random_graph()

# Создаем графический интерфейс
root = tk.Tk()
root.title("Поиск достижимых вершин")

# Создаем фигуру и оси для исходного графа
fig, ax = plt.subplots(figsize=(6, 4))
pos = nx.spring_layout(G)

# Рисуем исходный граф
nx.draw_networkx_nodes(G, pos, node_size=500, node_color="lightblue", ax=ax)
nx.draw_networkx_edges(G, pos, arrowstyle="->", arrowsize=20, ax=ax)
nx.draw_networkx_labels(G, pos, ax=ax)
ax.set_title("Исходный граф")

# Встраиваем график в окно
canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)

# Создаем элементы интерфейса
frame = tk.Frame(root)
frame.pack(side=tk.BOTTOM, pady=10)

label = tk.Label(frame, text="Введите начальную вершину:")
label.pack(side=tk.LEFT, padx=5)

entry = tk.Entry(frame)
entry.pack(side=tk.LEFT, padx=5)

button = tk.Button(frame, text="Найти достижимые вершины", command=on_button_click)
button.pack(side=tk.LEFT, padx=5)

root.mainloop()
