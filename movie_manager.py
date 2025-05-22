# Zmodyfikowany movie_manager.py z dodatkowymi sprawdzeniami
import json
import os
from movie import Movie

DATA_FILE = "movies.json"

class MovieManager:
    def __init__(self):
        self.movies = []
        self.load_movies()

    def add_movie(self, movie):
        if not movie.title:
            raise ValueError("Tytuł filmu nie może być pusty.")
        if not (0.0 <= movie.rating <= 10.0):
            raise ValueError("Ocena musi być z zakresu 0.0 - 10.0")
        if self._movie_exists(movie):
            raise ValueError("Film o takim tytule, reżyserze i roku już istnieje.")
        self.movies.append(movie)
        self.save_movies()

    def update_movie(self, index, new_movie):
        if not (0.0 <= new_movie.rating <= 10.0):
            raise ValueError("Ocena musi być z zakresu 0.0 - 10.0")
        # Sprawdzenie duplikatu z pominięciem tego indeksu
        for i, m in enumerate(self.movies):
            if i != index and m.title == new_movie.title and m.director == new_movie.director and m.year == new_movie.year:
                raise ValueError("Inny film o takim tytule, reżyserze i roku już istnieje.")
        self.movies[index] = new_movie
        self.save_movies()

    def delete_movie(self, index):
        del self.movies[index]
        self.save_movies()

    def search_movies(self, query):
        query_lower = query.lower()
        return [m for m in self.movies if query_lower in m.title.lower()]

    def load_movies(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.movies = [Movie(**d) for d in data]

    def save_movies(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump([m.to_dict() for m in self.movies], f, ensure_ascii=False, indent=2)

    def _movie_exists(self, movie):
        for m in self.movies:
            if m.title == movie.title and m.director == movie.director and m.year == movie.year:
                return True
        return False
