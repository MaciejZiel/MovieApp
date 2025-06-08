from tkinter import messagebox

# Dodanie nowego filmu do listy
def add_movie(app):
    movie = app.get_movie_from_fields()
    if not movie:
        return
    try:
        app.manager.add_movie(movie)
        app.clear_fields()
        app.reset_filters()
        messagebox.showinfo("Sukces", "Film dodany.")
    except ValueError as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas dodawania filmu: {e}")

# Edytuj zaznaczony film
def edit_movie(app):
    if app.selected_index is None:
        messagebox.showwarning("Brak wyboru", "Wybierz film do edycji.")
        return
    movie = app.get_movie_from_fields()
    if not movie:
        return
    actual_index = app.manager.movies.index(app.filtered_movies[app.selected_index])
    try:
    # Zachowanie istniejących komentarzy
        movie.comments = app.manager.movies[actual_index].comments
        app.manager.edit_movie(actual_index, movie)
        app.clear_fields()
        app.reset_filters()
        messagebox.showinfo("Sukces", "Film edytowany.")
    except (ValueError, IndexError) as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas edycji filmu: {e}")

# Usuń zaznaczony film
def delete_movie(app):
    if app.selected_index is None:
        messagebox.showwarning("Brak wyboru", "Wybierz film do usunięcia.")
        return
    actual_index = app.manager.movies.index(app.filtered_movies[app.selected_index])
    try:
        app.manager.delete_movie(actual_index)
        app.clear_fields()
        app.reset_filters()
        messagebox.showinfo("Sukces", "Film usunięty.")
    except IndexError as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas usuwania filmu: {e}")

# Eksport filmów do pliku
def export_movies_to_txt(app):
    try:
        with open("lista_filmow.txt", "w", encoding="utf-8") as f:
            for movie in app.manager.movies:
                f.write(f"Tytuł: {movie.title}\n")
                f.write(f"Reżyser: {movie.director}\n")
                f.write(f"Rok: {movie.year}\n")
                f.write(f"Gatunek: {movie.genre}\n")
                f.write(f"Status: {movie.status}\n")
                f.write(f"Ocena: {movie.rating}\n")
                f.write(f"Opis: {movie.description}\n")
                if movie.watch_date is not None:
                    f.write(f"Data obejrzenia: {movie.watch_date}\n")
                if movie.comments:
                    f.write("Komentarze:\n")
                    for c in movie.comments:
                        f.write(f" - {c}\n")
                f.write("\n" + "-" * 60 + "\n\n")
        messagebox.showinfo("Sukces", "Filmy wyeksportowano do pliku 'eksport_filmow.txt'.")
    except Exception as e:
        messagebox.showerror("Błąd", f"Wystąpił problem podczas eksportu: {e}")

# Generuje wykresy
def generate_charts(app):
    import matplotlib.pyplot as plt
    from collections import Counter, defaultdict

    if not app.manager.movies:
        messagebox.showinfo("Brak danych", "Brak filmów do analizy.")
        return
    genres = [m.genre for m in app.manager.movies]
    genre_counts = Counter(genres)

    genre_ratings = defaultdict(list)
    for m in app.manager.movies:
        genre_ratings[m.genre].append(m.rating)
    avg_ratings = {genre: sum(ratings) / len(ratings) for genre, ratings in genre_ratings.items()}

    status_counts = Counter(m.status for m in app.manager.movies)

    # Rysowanie wykresów
    plt.figure(figsize=(14, 4))

    plt.subplot(1, 3, 1)
    plt.bar(genre_counts.keys(), genre_counts.values(), color="skyblue")
    plt.title("Liczba filmów wg gatunku")
    plt.xticks(rotation=45, ha="right")

    plt.subplot(1, 3, 2)
    plt.bar(avg_ratings.keys(), avg_ratings.values(), color="lightgreen")
    plt.title("Średnia ocena wg gatunku")
    plt.xticks(rotation=45, ha="right")
    plt.ylim(0, 10)

    plt.subplot(1, 3, 3)
    plt.pie(status_counts.values(), labels=status_counts.keys(), autopct='%1.1f%%', startangle=90, colors=plt.cm.Paired.colors)
    plt.title("Status filmów")

    plt.tight_layout()
    plt.show()
