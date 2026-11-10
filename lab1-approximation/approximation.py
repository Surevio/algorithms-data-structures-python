import tkinter as tk
from tkinter import ttk
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.linalg import solve
import pandas as pd

def f(x):
  return (x**2 - 1) * 10**(-2*x)

def mnk(x, y, degree):
    A = np.zeros((degree + 1, degree + 1))
    B = np.zeros(degree + 1)
    for i in range(degree + 1):
        for j in range(degree + 1):
            A[i, j] = np.sum(x**(i + j))
        B[i] = np.sum(y * x**i)
    coeffs = solve(A, B)
    return coeffs

def poly(x, coeffs):
    return np.sum([coeffs[i] * x**i for i in range(len(coeffs))], axis=0)

def lagrange(x, x_data, y_data):
    n = len(x_data)
    y = np.zeros_like(x)
    for i in range(n):
        term = np.ones_like(x)
        for j in range(n):
            if i != j:
                term *= (x - x_data[j]) / (x_data[i] - x_data[j])
        y += y_data[i] * term
    return y

def calculate_and_plot():
    try:
        a = float(entry_a.get())
        b = float(entry_b.get())
        n = int(entry_n.get())
        if n < 1:
            raise ValueError("n должно быть больше 0")
        if a >= b:
            raise ValueError("a должно быть меньше b")

        dx = (b - a) / n
        x = np.linspace(a, b, n + 1)
        y_exact = f(x)
        x_int = x[:-1] + dx / 2
        y_lagrange = lagrange(x_int, x, y_exact)

        degrees = [2, 3, 4, 5]
        coeffs_list = [mnk(x, y_exact, degree) for degree in degrees]
        y_mnk_list = [poly(x, coeffs) for coeffs in coeffs_list]

        # Табулированные значения и погрешности МНК - измененный вывод
        output_string = ""
        for i, degree in enumerate(degrees):
            y_mnk = y_mnk_list[i]
            abs_errors = np.abs(y_exact - y_mnk)
            rel_errors = np.divide(abs_errors, np.abs(y_exact), out=np.zeros_like(abs_errors), where=np.abs(y_exact) != 0)
            max_abs_error = np.max(abs_errors)
            max_rel_error = np.max(rel_errors)

            output_string += f"Степень полинома: {degree}\n"
            output_string += f"Максимальная абсолютная погрешность: {max_abs_error:.4e}\n"
            output_string += f"Максимальная относительная погрешность: {max_rel_error:.4e}\n\n"


        # Погрешности Лагранжа
        abs_errors_lagrange = np.abs(y_lagrange - f(x_int))
        max_error_lagrange = np.max(abs_errors_lagrange)

        # Графики
        fig_mnk, ax_mnk = plt.subplots(figsize=(6, 4))
        ax_mnk.plot(x, y_exact, 'o', label='Точные значения')
        for i, degree in enumerate(degrees):
            ax_mnk.plot(x, y_mnk_list[i], label=f'МНК {degree}-й степени')
        ax_mnk.set_xlabel('x')
        ax_mnk.set_ylabel('y')
        ax_mnk.legend()
        ax_mnk.grid(True)
        fig_mnk.suptitle('Метод наименьших квадратов')
        plt.show(block=False)

        fig_lagrange, ax_lagrange = plt.subplots(figsize=(6, 4))
        ax_lagrange.plot(x_int, y_lagrange, 'o-', label='Интерполяция Лагранжа')
        ax_lagrange.plot(x, y_exact, 'x', label='Точные значения')
        ax_lagrange.set_xlabel('x')
        ax_lagrange.set_ylabel('y')
        ax_lagrange.legend()
        ax_lagrange.grid(True)
        ax_lagrange.set_title(f'Интерполяция Лагранжа (макс. ошибка: {max_error_lagrange:.4e})')
        plt.show(block=False)

        text_output.delete('1.0', tk.END)
        text_output.insert(tk.END, output_string)
        text_output.insert(tk.END, f"\nИнтерполяция Лагранжа:\nМаксимальная абсолютная погрешность: {max_error_lagrange:.4e}\n")

    except ValueError as e:
        error_label.config(text=f"Ошибка: {e}")
    except Exception as e:
        error_label.config(text=f"Ошибка: {e}")

root = tk.Tk()
root.title("Аппроксимация и интерполяция")

mainframe = ttk.Frame(root, padding=10)
mainframe.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Input Frame
input_frame = ttk.LabelFrame(mainframe, text="Входные данные")
input_frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

label_a = ttk.Label(input_frame, text="a:")
label_a.grid(row=0, column=0, sticky=tk.W)
entry_a = ttk.Entry(input_frame, width=10)
entry_a.insert(0, "0")
entry_a.grid(row=0, column=1)

label_b = ttk.Label(input_frame, text="b:")
label_b.grid(row=1, column=0, sticky=tk.W)
entry_b = ttk.Entry(input_frame, width=10)
entry_b.insert(0, "1")
entry_b.grid(row=1, column=1)

label_n = ttk.Label(input_frame, text="n:")
label_n.grid(row=2, column=0, sticky=tk.W)
entry_n = ttk.Entry(input_frame, width=10)
entry_n.insert(0, "5")
entry_n.grid(row=2, column=1)

button_calculate = ttk.Button(input_frame, text="Рассчитать и построить график", command=calculate_and_plot)
button_calculate.grid(row=3, column=0, columnspan=2)

error_label = ttk.Label(input_frame, text="", foreground="red")
error_label.grid(row=4, column=0, columnspan=2)

# Output Frame
output_frame = ttk.LabelFrame(mainframe, text="Результаты")
output_frame.grid(row=1, column=0, sticky="nsew")

text_output = tk.Text(output_frame, wrap=tk.WORD)
text_output.grid(row=0, column=0, sticky="nsew")

root.mainloop()
