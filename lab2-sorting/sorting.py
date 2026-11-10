import tkinter as tk
from tkinter import filedialog, messagebox
import random
import time
import os
import heapq

def generate_array(size, min_val, max_val):
    try:
        size = int(size)
        min_val = int(min_val)
        max_val = int(max_val)
        if size <= 0 or min_val >= max_val:
            raise ValueError("Некорректные параметры массива")
        return [random.randint(min_val, max_val) for _ in range(size)]
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка при генерации массива: {e}")
        return None

def read_array_from_file(filename):
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            arr = [int(x) for x in f.read().split()]
            if not arr:
                raise ValueError("Файл пустой или содержит некорректные данные")
            return arr
    except FileNotFoundError:
        return []  # Возвращаем пустой список, если файл не существует
    except ValueError as e:
        messagebox.showerror("Ошибка", f"Ошибка при чтении файла: {e}")
        return None

def bubble_sort(arr):
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr

def radix_sort(arr):
    if not arr:
        return arr
    max_num = max(arr)
    exp = 1
    while max_num // exp > 0:
        counting_sort(arr, exp)
        exp *= 10
    return arr

def counting_sort(arr, exp):
    n = len(arr)
    output = [0] * n
    count = [0] * 10

    for i in range(n):
        index = (arr[i] // exp) % 10
        count[index] += 1

    for i in range(1, 10):
        count[i] += count[i - 1]

    i = n - 1
    while i >= 0:
        index = (arr[i] // exp) % 10
        output[count[index] - 1] = arr[i]
        count[index] -= 1
        i -= 1

    for i in range(n):
        arr[i] = output[i]

def pancake_sort(arr):
    n = len(arr)
    for i in range(n, 0, -1):
        max_index = arr.index(max(arr[:i]))
        flip(arr, max_index)
        flip(arr, i - 1)
    return arr

def flip(arr, k):
    l, r = 0, k
    while l < r:
        arr[l], arr[r] = arr[r], arr[l]
        l += 1
        r -= 1

def bitonic_sort(arr):
    n = len(arr)
    if n <= 1:
        return arr
    mid = n // 2
    left = bitonic_sort(arr[:mid])
    right = bitonic_sort(arr[mid:])
    arr = bitonic_merge(left + right)
    return arr

def bitonic_merge(arr):
    n = len(arr)
    if n <= 1:
        return arr
    dist = n // 2
    for i in range(dist):
        if arr[i] > arr[i + dist]:
            arr[i], arr[i + dist] = arr[i + dist], arr[i]
    left = bitonic_merge(arr[:dist])
    right = bitonic_merge(arr[dist:])
    return left + right

def heapsort(arr):
    heapq.heapify(arr)
    return [heapq.heappop(arr) for _ in range(len(arr))]

def save_array_to_file(arr, filename="array.txt"):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(' '.join(map(str, arr)))
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка при записи в файл: {e}")
        return False

def save_results_to_file(algorithm, time_taken, original_array, sorted_array):
    try:
        with open("results.txt", "a", encoding='utf-8') as f:
            f.write(f"\nАлгоритм: {algorithm}\n")
            f.write(f"Время выполнения: {time_taken:.6f} секунд\n")
            f.write(f"Исходный массив (первые 50): {original_array[:50]}\n")
            f.write(f"Отсортированный массив (первые 50): {sorted_array[:50]}\n")
            f.write("-" * 50 + "\n")
        return True
    except Exception as e:
        messagebox.showerror("Ошибка", f"Ошибка записи результатов в файл: {e}")
        return False

def sort_and_display():
    try:
        selected_array = random_array if array_var.get() == 1 else file_array
        if selected_array is None:
            raise ValueError("Массив не выбран")
        if len(selected_array) == 0:
            raise ValueError("Массив пуст")

        result_text.delete(1.0, tk.END)
        results = {}
        
        for algo_name, algo_func in sorting_algorithms.items():
            try:
                start_time = time.time()
                sorted_array = algo_func(selected_array.copy())
                end_time = time.time()
                time_taken = end_time - start_time
                results[algo_name] = time_taken
                result_text.insert(tk.END, f"{algo_name}: {time_taken:.6f} секунд\n")
                result_text.see(tk.END)
                root.update()
                save_results_to_file(algo_name, time_taken, selected_array, sorted_array)
            except Exception as e:
                result_text.insert(tk.END, f"{algo_name}: Ошибка - {e}\n")

        non_library_results = {k: v for k, v in results.items() if k != "Библиотечная сортировка"}
        if non_library_results:
            fastest_non_library_algorithm = min(non_library_results, key=non_library_results.get)
            result_text.insert(tk.END,
                               f"\nСамый быстрый алгоритм (без учёта библиотечного): {fastest_non_library_algorithm}\n")
        else:
            result_text.insert(tk.END, "\nНет результатов для сравнения\n")

    except ValueError as e:
        messagebox.showerror("Ошибка", str(e))
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла неизвестная ошибка: {e}")

def generate_array_gui():
    global random_array
    random_array = generate_array(size_entry.get(), min_entry.get(), max_entry.get())
    if random_array and save_array_to_file(random_array):
        result_text.insert(tk.END, f"Массив сгенерирован и сохранен в array.txt\n")
        result_text.insert(tk.END, f"Первые 10 элементов: {random_array[:10]}\n")

def read_array_from_file_gui():
    global file_array
    file_array = read_array_from_file("array.txt")
    if file_array is not None:
        result_text.insert(tk.END, f"Массив прочитан из array.txt\n")
        result_text.insert(tk.END, f"Первые 10 элементов: {file_array[:10]}\n")
    else:
        result_text.insert(tk.END, "Файл array.txt пуст или содержит некорректные данные\n")

# Глобальные переменные
random_array = None
file_array = None

# Создание основного окна
root = tk.Tk()
root.title("Сортировка массивов")
root.geometry("600x500")

# Создание виджетов
size_label = tk.Label(root, text="Размер массива:")
size_entry = tk.Entry(root)
min_label = tk.Label(root, text="Мин. значение:")
min_entry = tk.Entry(root)
max_label = tk.Label(root, text="Макс. значение:")
max_entry = tk.Entry(root)

generate_button = tk.Button(root, text="Сгенерировать массив", command=generate_array_gui)
load_button = tk.Button(root, text="Загрузить из файла", command=read_array_from_file_gui)

array_var = tk.IntVar(value=1)
radio_random = tk.Radiobutton(root, text="Случайный массив", variable=array_var, value=1)
radio_file = tk.Radiobutton(root, text="Массив из файла", variable=array_var, value=2)

sort_button = tk.Button(root, text="Запустить сортировку", command=sort_and_display)

# Создание текстового поля с прокруткой
text_frame = tk.Frame(root)
text_frame.grid(row=8, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
root.grid_rowconfigure(8, weight=1)
root.grid_columnconfigure(0, weight=1)

result_text = tk.Text(text_frame, height=15, width=70, wrap=tk.WORD)
scrollbar = tk.Scrollbar(text_frame, command=result_text.yview)
result_text.configure(yscrollcommand=scrollbar.set)

result_text.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Размещение виджетов
size_label.grid(row=0, column=0, sticky="w", padx=5, pady=2)
size_entry.grid(row=0, column=1, padx=5, pady=2)
min_label.grid(row=1, column=0, sticky="w", padx=5, pady=2)
min_entry.grid(row=1, column=1, padx=5, pady=2)
max_label.grid(row=2, column=0, sticky="w", padx=5, pady=2)
max_entry.grid(row=2, column=1, padx=5, pady=2)
generate_button.grid(row=3, column=0, columnspan=2, pady=2)
load_button.grid(row=4, column=0, columnspan=2, pady=2)
radio_random.grid(row=5, column=0, columnspan=2, pady=2)
radio_file.grid(row=6, column=0, columnspan=2, pady=2)
sort_button.grid(row=7, column=0, columnspan=2, pady=5)

sorting_algorithms = {
    "Сортировка пузырьком": bubble_sort,
    "Поразрядная сортировка": radix_sort,
    "Блинная сортировка": pancake_sort,
    "Битоническая сортировка": bitonic_sort,
    "Библиотечная сортировка": lambda x: sorted(x),
}

# Установка значений по умолчанию
size_entry.insert(0, "10")
min_entry.insert(0, "1")
max_entry.insert(0, "100")

root.mainloop()