import json
from datetime import datetime
from movie import Movie

class MovieManager:
    def __init__(self, filename="movies.json"):
        self.filename = filename
        self.movies = []
        self.load()

    # Wczytuje filmy z pliku
    def load(self):
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.movies = [Movie(**movie) for movie in data]
        except (FileNotFoundError, json.JSONDecodeError):
            self.movies = []

    # Zapisuje aktualną listę filmów
    def save(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            data = [movie.to_dict() for movie in self.movies]
            json.dump(data, f, ensure_ascii=False, indent=4)

    # Dodaje nowy film i zapisuje
    def add_movie(self, movie):
        if movie.watch_date is not None and movie.status == "Obejrzany":
            movie.watch_date = datetime.now().strftime("%Y-%m-%d")
        self.movies.append(movie)
        self.save()


    # Edytuje wskazany film
    def edit_movie(self, index, movie):
        old_status = self.movies[index].status
        new_status = movie.status

        # Ustaw datę obejrzenia, jeśli zmieniono status na „Obejrzany”
        if old_status != "Obejrzany" and new_status == "Obejrzany":
            movie.watch_date = datetime.now().strftime("%Y-%m-%d")
        elif new_status != "Obejrzany":
            movie.watch_date = None

        self.movies[index] = movie
        self.save()

    # Usuwanie film z listy
    def delete_movie(self, index):
        del self.movies[index]
        self.save()
