# Zmodyfikowany movie_app.py z dynamicznymi polami 'Reżyser' i 'Rok'
import tkinter as tk
from tkinter import ttk, messagebox
from movie import Movie
from movie_manager import MovieManager

class MovieApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Watchlist – Kolekcja Filmów")
        self.manager = MovieManager()
        self.selected_index = None
        self.sort_column = None
        self.sort_reverse = False
        self.genre_options = ["Akcja", "Dramat", "Kryminalny", "Thriller", "Sci-Fi", "Muzyczny"]

        self.setup_ui()
        self.refresh_movie_list()

    def setup_ui(self):
        frame = tk.Frame(self.root)
        frame.pack(padx=10, pady=10)
        labels = ["Tytuł", "Reżyser", "Rok", "Gatunek", "Status", "Ocena", "Opis"]
        for i, text in enumerate(labels):
            tk.Label(frame, text=text).grid(row=i, column=0)

        self.vars = [tk.StringVar() for _ in labels]

        for i, var in enumerate(self.vars):
            if labels[i] == "Status":
                self.status_combobox = ttk.Combobox(frame, textvariable=var, values=["Obejrzany", "Do obejrzenia"], state="readonly", width=47)
                self.status_combobox.grid(row=i, column=1)
            elif labels[i] == "Gatunek":
                self.genre_combobox = ttk.Combobox(frame, textvariable=var, values=self.genre_options, width=47)
                self.genre_combobox.grid(row=i, column=1)
            else:
                tk.Entry(frame, textvariable=var, width=50).grid(row=i, column=1)

        tk.Button(frame, text="Dodaj film", command=self.add_movie).grid(row=7, column=0, pady=5)
        tk.Button(frame, text="Edytuj film", command=self.edit_movie).grid(row=7, column=1, pady=5)
        tk.Button(frame, text="Usuń film", command=self.delete_movie).grid(row=8, column=0, columnspan=2, pady=5)

        filter_frame = ttk.LabelFrame(self.root, text="Filtruj filmy", padding=(10, 5))
        filter_frame.pack(padx=10, pady=10, fill="x")

        tk.Label(filter_frame, text="Tytuł:").grid(row=0, column=0, sticky="w", padx=5, pady=2)
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(filter_frame, textvariable=self.search_var, width=20)
        search_entry.grid(row=0, column=1, padx=5, pady=2)
        search_entry.bind("<KeyRelease>", self.live_search)

        tk.Label(filter_frame, text="Status:").grid(row=0, column=2, sticky="w", padx=5, pady=2)
        self.filter_status = tk.StringVar()
        self.filter_status_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_status, values=["", "Obejrzany", "Do obejrzenia"], state="readonly", width=18)
        self.filter_status_combobox.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(filter_frame, text="Gatunek:").grid(row=1, column=0, sticky="w", padx=5, pady=2)
        self.filter_genre = tk.StringVar()
        self.filter_genre_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_genre, values=["", *self.genre_options], state="readonly", width=18)
        self.filter_genre_combobox.grid(row=1, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="Reżyser:").grid(row=1, column=2, sticky="w", padx=5, pady=2)
        self.filter_director = tk.StringVar()
        self.filter_director_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_director, state="readonly", width=18)
        self.filter_director_combobox.grid(row=1, column=3, padx=5, pady=2)

        tk.Label(filter_frame, text="Rok:").grid(row=2, column=0, sticky="w", padx=5, pady=2)
        self.filter_year = tk.StringVar()
        self.filter_year_combobox = ttk.Combobox(filter_frame, textvariable=self.filter_year, state="readonly", width=8)
        self.filter_year_combobox.grid(row=2, column=1, padx=5, pady=2)

        tk.Button(filter_frame, text="Filtruj", command=self.apply_filters).grid(row=2, column=3, padx=5, pady=5, sticky="e")

        columns = ("Tytuł", "Rok", "Gatunek", "Status", "Ocena")
        self.tree = ttk.Treeview(self.root, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col, command=lambda c=col: self.sort_by_column(c))
            self.tree.column(col, width=100)
        self.tree.pack(padx=10, pady=10)
        self.tree.bind("<ButtonRelease-1>", self.on_tree_select)

        self.update_filter_options()

    def update_filter_options(self):
        directors = sorted(set(m.director for m in self.manager.movies))
        years = sorted(set(str(m.year) for m in self.manager.movies))
        self.filter_director_combobox['values'] = [""] + directors
        self.filter_year_combobox['values'] = [""] + years

    def get_movie_from_fields(self):
        try:
            genre = self.vars[3].get()
            if genre not in self.genre_options:
                self.genre_options.append(genre)
                self.genre_combobox['values'] = self.genre_options
                self.filter_genre_combobox['values'] = ["", *self.genre_options]
            return Movie(
                self.vars[0].get(), self.vars[1].get(), int(self.vars[2].get()),
                genre, self.vars[4].get(), float(self.vars[5].get()), self.vars[6].get()
            )
        except ValueError as ve:
            messagebox.showerror("Błąd danych", str(ve))
            return None

    def add_movie(self):
        movie = self.get_movie_from_fields()
        if movie:
            if any(m.title.lower() == movie.title.lower() and m.director.lower() == movie.director.lower() for m in self.manager.movies):
                messagebox.showerror("Błąd", "Film o tym tytule i reżyserze już istnieje.")
                return
            try:
                self.manager.add_movie(movie)
                self.clear_fields()
                self.refresh_movie_list()
                self.update_filter_options()
                messagebox.showinfo("Sukces", "Film dodany.")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def edit_movie(self):
        if self.selected_index is None:
            messagebox.showwarning("Brak wyboru", "Wybierz film z listy.")
            return
        movie = self.get_movie_from_fields()
        if movie:
            if any(i != self.selected_index and m.title.lower() == movie.title.lower() and m.director.lower() == movie.director.lower()
                   for i, m in enumerate(self.manager.movies)):
                messagebox.showerror("Błąd", "Inny film o tym tytule i reżyserze już istnieje.")
                return
            try:
                self.manager.update_movie(self.selected_index, movie)
                self.clear_fields()
                self.refresh_movie_list()
                self.update_filter_options()
                self.selected_index = None
                messagebox.showinfo("Sukces", "Film zaktualizowany.")
            except Exception as e:
                messagebox.showerror("Błąd", str(e))

    def delete_movie(self):
        if self.selected_index is None:
            messagebox.showwarning("Brak wyboru", "Wybierz film do usunięcia.")
            return
        self.manager.delete_movie(self.selected_index)
        self.clear_fields()
        self.refresh_movie_list()
        self.update_filter_options()
        self.selected_index = None
        messagebox.showinfo("Sukces", "Film usunięty.")

    def on_tree_select(self, event):
        item = self.tree.selection()
        if item:
            index = self.tree.index(item[0])
            movie = self.manager.movies[index]
            for var, val in zip(self.vars, [
                movie.title, movie.director, movie.year, movie.genre,
                movie.status, movie.rating, movie.description
            ]):
                var.set(val)
            self.selected_index = index

    def live_search(self, event):
        self.apply_filters()

    def apply_filters(self):
        query = self.search_var.get().lower()
        status = self.filter_status.get().lower()
        genre = self.filter_genre.get().lower()
        director = self.filter_director.get().lower()
        year = self.filter_year.get()
        results = [m for m in self.manager.movies if query in m.title.lower()]
        if status:
            results = [m for m in results if m.status.lower() == status]
        if genre:
            results = [m for m in results if m.genre.lower() == genre]
        if director:
            results = [m for m in results if director in m.director.lower()]
        if year.isdigit():
            results = [m for m in results if m.year == int(year)]
        self.display_movies(results)

    def sort_by_column(self, col):
        col_map = {
            "Tytuł": lambda m: m.title.lower(),
            "Rok": lambda m: m.year,
            "Gatunek": lambda m: m.genre.lower(),
            "Status": lambda m: m.status.lower(),
            "Ocena": lambda m: m.rating
        }
        if col == self.sort_column:
            self.sort_reverse = not self.sort_reverse
        else:
            self.sort_reverse = False
            self.sort_column = col
        sorted_movies = sorted(self.manager.movies, key=col_map[col], reverse=self.sort_reverse)
        self.display_movies(sorted_movies)

    def display_movies(self, movie_list):
        self.tree.delete(*self.tree.get_children())
        for m in movie_list:
            self.tree.insert("", tk.END, values=(m.title, m.year, m.genre, m.status, m.rating))

    def refresh_movie_list(self):
        self.display_movies(self.manager.movies)

    def clear_fields(self):
        for var in self.vars:
            var.set("")
