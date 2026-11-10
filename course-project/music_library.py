import tkinter as tk
from tkinter import messagebox
import json

# Список для хранения альбомов
albums = []

# Множество для хранения уникальных жанров
genres = set()

# Класс для реализации дерева (иерархия исполнителей и их альбомов)
class ArtistNode:
    def __init__(self, name):
        self.name = name
        self.albums = []
        self.children = []

    def add_album(self, album):
        self.albums.append(album)

    def add_child(self, child):
        self.children.append(child)

# Функция для сохранения данных в файл
def save_data_to_file():
    data = {
        "albums": albums,
        "genres": list(genres)
    }
    with open("music_library.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    messagebox.showinfo("Сохранение", "Данные успешно сохранены в файл.")

# Функция для загрузки данных из файла
def load_data_from_file():
    global albums, genres
    try:
        with open("music_library.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            albums = data.get("albums", [])
            genres = set(data.get("genres", []))
        messagebox.showinfo("Загрузка", "Данные успешно загружены из файла.")
    except FileNotFoundError:
        messagebox.showwarning("Ошибка", "Файл с данными не найден.")

# Функция для добавления альбома
def add_album(artist, title, genre, year):
    album = {
        "artist": artist,
        "title": title,
        "genre": genre,
        "year": year
    }
    albums.append(album)
    genres.add(genre)
    messagebox.showinfo("Успех", f"Альбом '{title}' исполнителя '{artist}' добавлен.")

# Функция для поиска альбомов по исполнителю
def find_albums_by_artist(artist):
    result = [album for album in albums if album["artist"] == artist]
    if result:
        messagebox.showinfo("Результат", f"Альбомы исполнителя '{artist}':\n" +
                            "\n".join([f"- {album['title']} ({album['year']})" for album in result]))
    else:
        messagebox.showinfo("Результат", f"Альбомы исполнителя '{artist}' не найдены.")

# Функция для вывода всех жанров
def list_genres():
    messagebox.showinfo("Жанры", "Жанры в библиотеке:\n" + "\n".join([f"- {genre}" for genre in genres]))

# Функция для вывода всех исполнителей из библиотеки
def list_artists():
    artists = set(album["artist"] for album in albums)
    if artists:
        messagebox.showinfo("Исполнители", "Исполнители в библиотеке:\n" + "\n".join([f"- {artist}" for artist in artists]))
    else:
        messagebox.showinfo("Исполнители", "В библиотеке пока нет исполнителей.")

# Функция для создания иерархии исполнителей
def create_artist_hierarchy():
    root = ArtistNode("Музыкальные исполнители")
    artists = set(album["artist"] for album in albums)

    # Группируем исполнителей по жанрам
    genre_groups = {}
    for album in albums:
        genre = album["genre"]
        artist = album["artist"]
        if genre not in genre_groups:
            genre_groups[genre] = []
        if artist not in genre_groups[genre]:
            genre_groups[genre].append(artist)

    # Создаем иерархию
    for genre, artists in genre_groups.items():
        genre_node = ArtistNode(genre)
        root.add_child(genre_node)
        for artist in artists:
            artist_node = ArtistNode(artist)
            genre_node.add_child(artist_node)

    return root

# Функция для вывода иерархии исполнителей
def print_hierarchy(node, level=0):
    result = "  " * level + node.name + "\n"
    for child in node.children:
        result += print_hierarchy(child, level + 1)
    return result

# Функция для отображения иерархии в GUI
def show_hierarchy():
    hierarchy = create_artist_hierarchy()
    hierarchy_text = print_hierarchy(hierarchy)
    messagebox.showinfo("Иерархия исполнителей", hierarchy_text)

# Основной код для создания GUI
def main():
    # Создаем главное окно
    root = tk.Tk()
    root.title("Библиотека меломана")
    root.geometry("350x500")

    # Создаем метки и поля ввода
    tk.Label(root, text="Исполнитель:").grid(row=0, column=0, padx=10, pady=10)
    artist_entry = tk.Entry(root, width=30)
    artist_entry.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(root, text="Название альбома:").grid(row=1, column=0, padx=10, pady=10)
    title_entry = tk.Entry(root, width=30)
    title_entry.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(root, text="Жанр:").grid(row=2, column=0, padx=10, pady=10)
    genre_entry = tk.Entry(root, width=30)
    genre_entry.grid(row=2, column=1, padx=10, pady=10)

    tk.Label(root, text="Год выпуска:").grid(row=3, column=0, padx=10, pady=10)
    year_entry = tk.Entry(root, width=30)
    year_entry.grid(row=3, column=1, padx=10, pady=10)

    # Кнопка для добавления альбома
    def add_album_button_click():
        artist = artist_entry.get()
        title = title_entry.get()
        genre = genre_entry.get()
        year = year_entry.get()
        if artist and title and genre and year:
            add_album(artist, title, genre, year)
            artist_entry.delete(0, tk.END)
            title_entry.delete(0, tk.END)
            genre_entry.delete(0, tk.END)
            year_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Заполните все поля!")

    tk.Button(root, text="Добавить альбом", command=add_album_button_click).grid(row=4, column=0, columnspan=2, pady=10)

    # Кнопка для поиска альбомов по исполнителю
    def find_albums_button_click():
        artist = artist_entry.get()
        if artist:
            find_albums_by_artist(artist)
            artist_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Ошибка", "Введите исполнителя!")

    tk.Button(root, text="Найти альбомы", command=find_albums_button_click).grid(row=5, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Показать жанры", command=list_genres).grid(row=6, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Показать исполнителей", command=list_artists).grid(row=7, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Показать иерархию исполнителей", command=show_hierarchy).grid(row=8, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Сохранить данные", command=save_data_to_file).grid(row=9, column=0, columnspan=2, pady=10)

    tk.Button(root, text="Загрузить данные", command=load_data_from_file).grid(row=10, column=0, columnspan=2, pady=10)

    root.mainloop()

# Запуск программы
if __name__ == "__main__":
    main()
