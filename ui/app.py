from movie import Movie
from movie_manager import MovieManager
from ui.components import setup_ui
from ui.filters import apply_filters, reset_filters, update_filter_options
from ui.handlers import add_movie, edit_movie, delete_movie, export_movies_to_txt, generate_charts
from ui.details import show_details, load_movie_into_fields
from ui.comments import add_comment_to_movie, add_comment_popup, add_comment_popup_external

class MovieApp:
    def __init__(self, root):
        self.tree = None
        import tkinter as tk
        self.root = root
        self.root.title("Movie Manager")

        self.manager = MovieManager()
        self.filtered_movies = []

        self.selected_index = None
        self.sort_column = None
        self.sort_reverse = False

        # Pola wejściowe
        self.vars = [tk.StringVar() for _ in range(7)]
        (self.title_var, self.director_var, self.year_var,
         self.genre_var, self.status_var, self.rating_var, self.desc_var) = self.vars

        # Pola filtrowania
        self.search_var = tk.StringVar()
        self.filter_status = tk.StringVar()
        self.filter_genre = tk.StringVar()
        self.filter_director = tk.StringVar()
        self.filter_year = tk.StringVar()

        # Związki akcji z metodami
        self.reset_filters = lambda: reset_filters(self)
        self.apply_filters = lambda: apply_filters(self)
        self.update_filter_options = lambda: update_filter_options(self)
        self.add_movie = lambda: add_movie(self)
        self.edit_movie = lambda: edit_movie(self)
        self.delete_movie = lambda: delete_movie(self)
        self.export_movies_to_txt = lambda: export_movies_to_txt(self)
        self.generate_charts = lambda: generate_charts(self)
        self.show_details = lambda: show_details(self)
        self.load_movie_into_fields = lambda movie: load_movie_into_fields(self, movie)
        self.add_comment_popup_external = lambda: add_comment_popup_external(self)
        self.add_comment_to_movie = lambda c: add_comment_to_movie(self, c)
        self.add_comment_popup = lambda m: add_comment_popup(self, m)

        setup_ui(self)
        self.reset_filters()

    def clear_fields(self):
        for var in self.vars:
            var.set("")
        if self.tree.selection():
            self.tree.selection_remove(self.tree.selection())
        self.selected_index = None

    def refresh_movie_list(self):
        selected_movie = None
        if self.selected_index is not None and 0 <= self.selected_index < len(self.filtered_movies):
            selected_movie = self.filtered_movies[self.selected_index]

        self.tree.delete(*self.tree.get_children())
        for movie in self.filtered_movies:
            self.tree.insert("", "end", values=(
                movie.title, movie.year, movie.genre, movie.status, movie.rating))

        if selected_movie:
            for iid in self.tree.get_children():
                item = self.tree.item(iid)
                vals = item['values']
                if vals[0] == selected_movie.title and vals[1] == selected_movie.year:
                    self.tree.selection_set(iid)
                    break

    def on_tree_select(self, event):
        selected = self.tree.selection()
        if not selected:
            self.selected_index = None
            self.clear_fields()
            return
        item = self.tree.item(selected[0])
        values = item['values']
        for idx, movie in enumerate(self.filtered_movies):
            if movie.title == values[0] and str(movie.year) == str(values[1]):
                self.selected_index = idx
                self.load_movie_into_fields(movie)
                break

    # Pobiera dane z formularza i tworzy obiekt Movie
    def get_movie_from_fields(self, messagebox=None):
        try:
            year = int(self.year_var.get())
        except ValueError:
            messagebox.showerror("Błąd", "Rok musi być liczbą całkowitą.")
            return None

        try:
            rating = float(self.rating_var.get())
            if not (0 <= rating <= 10):
                raise ValueError("Ocena musi być od 0 do 10.")
        except ValueError:
            messagebox.showerror("Błąd", "Ocena musi być liczbą z przedziału od 0 do 10.")
            return None

        title = self.title_var.get().strip()
        director = self.director_var.get().strip()
        genre = self.genre_var.get().strip()
        status = self.status_var.get().strip()
        description = self.desc_var.get().strip()

        if not title or not director or not genre or not status:
            messagebox.showerror("Błąd", "Wypełnij wszystkie pola oprócz opisu.")
            return None

        return Movie(title, director, year, genre, status, rating, description)
