import tkinter as tk
from tkinter import messagebox
from random import randint
import time
import math

ARRAY_SIZE = 1000
RESULTS_FILE = "results1.txt"

# Функции поиска
def linear_search(arr, x):
    for i, val in enumerate(arr):
        if val == x:
            return i
    return -1

def sentinel_search(arr, x):
    n = len(arr)
    if n == 0:
        return -1
    last = arr[-1]
    arr[-1] = x
    i = 0
    while arr[i] != x:
        i += 1
    arr[-1] = last
    return i if i < n - 1 or last == x else -1

def interpolation_search(arr, x):
    low, high = 0, len(arr) - 1
    while low <= high and arr[low] <= x <= arr[high]:
        if low == high:
            return low if arr[low] == x else -1
        if arr[high] == arr[low]:
            break
        pos = low + ((x - arr[low]) * (high - low)) // (arr[high] - arr[low])
        if pos < low or pos > high:
            break
        if arr[pos] == x:
            return pos
        if arr[pos] < x:
            low = pos + 1
        else:
            high = pos - 1
    return -1

def jump_search(arr, x):
    n = len(arr)
    step = int(math.sqrt(n))
    prev = 0
    while prev < n and arr[min(step, n) - 1] < x:
        prev = step
        step += int(math.sqrt(n))
        if prev >= n:
            return -1
    for i in range(prev, min(step, n)):
        if arr[i] == x:
            return i
    return -1

# Словарь методов: имя (русское для интерфейса) и функция
METHODS_RU = {
    "Линейный": linear_search,
    "Дозорный": sentinel_search,
    "Интерполяционный": interpolation_search,
    "Прыжковый": jump_search
}

# Английские соответствия для записи в файл (без проблем с кодировкой)
METHODS_EN = {
    "Линейный": "linear",
    "Дозорный": "sentinel",
    "Интерполяционный": "interpolation",
    "Прыжковый": "jump"
}

# Основное приложение
class App:
    def __init__(self, root):
        self.root = root
        root.title("ЛР №3 – Вариант 30")
        root.geometry("800x650")

        # Данные
        self.arr_gen = []          # сгенерированный (отсортирован)
        self.arr_file = []          # исходный из файла
        self.arr_file_sorted = []   # отсортированный для файла

        self.create_widgets()

    def create_widgets(self):
        # Генератор
        tk.Label(self.root, text="Генератор случайных чисел", font=("Arial", 10, "bold")).place(x=10, y=5)

        tk.Label(self.root, text="Диапазон:").place(x=10, y=30)
        self.entry_a = tk.Entry(self.root, width=6)
        self.entry_a.place(x=80, y=30)
        tk.Label(self.root, text="-").place(x=125, y=30)
        self.entry_b = tk.Entry(self.root, width=6)
        self.entry_b.place(x=140, y=30)

        tk.Button(self.root, text="Сгенерировать", command=self.generate).place(x=200, y=27)

        # Отображение массива (текстовое поле с прокруткой)
        self.gen_text = tk.Text(self.root, height=3, width=90, wrap=tk.WORD, font=("Courier", 8))
        self.gen_text.place(x=10, y=55)
        scroll_gen = tk.Scrollbar(self.root, command=self.gen_text.yview)
        scroll_gen.place(x=740, y=55, height=50)
        self.gen_text.config(yscrollcommand=scroll_gen.set)

        # Поле ввода искомого
        tk.Label(self.root, text="Искомое (генератор):").place(x=10, y=115)
        self.entry_gen_val = tk.Entry(self.root, width=8)
        self.entry_gen_val.place(x=130, y=115)

        # Кнопки методов для генератора и метки результатов
        self.gen_results = []
        y = 145
        for i, name in enumerate(METHODS_RU.keys()):
            btn = tk.Button(self.root, text=name, command=lambda n=name: self.search_gen(n))
            btn.place(x=10, y=y + i*25)

            # Метка для результата
            lbl = tk.Label(self.root, text="-", fg="green", anchor="w", width=70)
            lbl.place(x=120, y=y + i*25)
            self.gen_results.append(lbl)

        # Файл
        tk.Label(self.root, text="Загрузка из файла", font=("Arial", 10, "bold")).place(x=10, y=270)

        tk.Button(self.root, text="Загрузить test.txt", command=self.load_file).place(x=10, y=295)
        self.lbl_file_info = tk.Label(self.root, text="", fg="darkblue")
        self.lbl_file_info.place(x=130, y=297)

        # Отображение массива из файла
        self.file_text = tk.Text(self.root, height=3, width=90, wrap=tk.WORD, font=("Courier", 8))
        self.file_text.place(x=10, y=325)
        scroll_file = tk.Scrollbar(self.root, command=self.file_text.yview)
        scroll_file.place(x=740, y=325, height=50)
        self.file_text.config(yscrollcommand=scroll_file.set)

        # Поле ввода искомого
        tk.Label(self.root, text="Искомое (файл):").place(x=10, y=385)
        self.entry_file_val = tk.Entry(self.root, width=8)
        self.entry_file_val.place(x=110, y=385)

        # Кнопки методов для файла
        self.file_results = []
        yf = 415
        for i, name in enumerate(METHODS_RU.keys()):
            btn = tk.Button(self.root, text=name, command=lambda n=name: self.search_file(n))
            btn.place(x=10, y=yf + i*25)

            lbl = tk.Label(self.root, text="-", fg="green", anchor="w", width=70)
            lbl.place(x=120, y=yf + i*25)
            self.file_results.append(lbl)

        # Пояснение про файл результатов
        tk.Label(self.root, text=f"Результаты дописываются в {RESULTS_FILE} (латиница)", fg="gray").place(x=10, y=600)

    # Логика
    def generate(self):
        try:
            a = int(self.entry_a.get())
            b = int(self.entry_b.get())
            if a > b:
                messagebox.showerror("Ошибка", "Начало > конца")
                return
            self.arr_gen = sorted([randint(a, b) for _ in range(ARRAY_SIZE)])
            # Покажем первые 50 элементов
            preview = " ".join(map(str, self.arr_gen[:50])) + (" …" if ARRAY_SIZE > 50 else "")
            self.gen_text.delete(1.0, tk.END)
            self.gen_text.insert(1.0, preview)
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целые числа")

    def load_file(self):
        try:
            with open("test.txt", "r", encoding="utf-8") as f:
                lines = [line.strip() for line in f if line.strip()]
                self.arr_file = [int(x) for x in lines[:ARRAY_SIZE]]
                self.arr_file_sorted = sorted(self.arr_file)
            self.lbl_file_info.config(text=f"Загружено {len(self.arr_file)} эл.")
            preview = " ".join(map(str, self.arr_file[:50])) + (" …" if len(self.arr_file) > 50 else "")
            self.file_text.delete(1.0, tk.END)
            self.file_text.insert(1.0, preview)
        except Exception as e:
            messagebox.showerror("Ошибка", f"Не удалось загрузить файл:\n{e}")

    def search_gen(self, method_name):
        if not self.arr_gen:
            messagebox.showwarning("Предупреждение", "Сначала сгенерируйте массив")
            return
        self._perform_search(method_name, self.arr_gen, self.entry_gen_val,
                             self.gen_results[list(METHODS_RU.keys()).index(method_name)], "generator")

    def search_file(self, method_name):
        if not self.arr_file:
            messagebox.showwarning("Предупреждение", "Сначала загрузите файл")
            return
        # Для методов, требующих сортировки, используем отсортированную копию
        if method_name in ("Интерполяционный", "Прыжковый"):
            arr_use = self.arr_file_sorted
        else:
            arr_use = self.arr_file
        self._perform_search(method_name, arr_use, self.entry_file_val,
                             self.file_results[list(METHODS_RU.keys()).index(method_name)], "file")

    def _perform_search(self, method_name, arr, entry, result_label, source):
        try:
            x = int(entry.get())
        except ValueError:
            messagebox.showerror("Ошибка", "Введите целое число")
            return

        func = METHODS_RU[method_name]
        start = time.perf_counter()
        idx = func(arr, x)
        elapsed = (time.perf_counter() - start) * 1000  # в миллисекундах

        # Формируем понятное сообщение
        if idx != -1:
            message = f"Значение {x} найдено, индекс: {idx}  ({elapsed:.3f} мс)"
        else:
            message = f"Значение {x} не найдено ({elapsed:.3f} мс)"
        result_label.config(text=message)

        # Запись в файл (латиница, чтобы избежать проблем с кодировкой)
        method_en = METHODS_EN[method_name]
        try:
            with open(RESULTS_FILE, "a", encoding="utf-8") as f:
                f.write(f"{source} | {method_en} | target={x} | index={idx} | time_ms={elapsed:.3f}\n")
        except:
            pass

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()