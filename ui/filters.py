# Pobieranianiea wartości z pól filtrujących
def apply_filters(app):
    title_filter = app.search_var.get().lower()
    status_filter = app.filter_status.get()
    genre_filter = app.filter_genre.get()
    director_filter = app.filter_director.get()
    year_filter = app.filter_year.get()

    # Zastosuj filtry
    app.filtered_movies = []
    for m in app.manager.movies:
        if title_filter and title_filter not in m.title.lower():
            continue
        if status_filter and m.status != status_filter:
            continue
        if genre_filter and m.genre != genre_filter:
            continue
        if director_filter and m.director != director_filter:
            continue
        if year_filter and str(m.year) != year_filter:
            continue
        app.filtered_movies.append(m)

    # Zresetuj sortowanie i odśwież view
    app.sort_column = None
    app.sort_reverse = False
    app.refresh_movie_list()
    app.update_filter_options()

def reset_filters(app):
    # Wyczyść wszystkie pola
    app.search_var.set("")
    app.filter_status.set("")
    app.filter_genre.set("")
    app.filter_director.set("")
    app.filter_year.set("")

    # Przywróć pełną listę filmów
    app.filtered_movies = app.manager.movies[:]
    app.refresh_movie_list()
    app.update_filter_options()

    # Zaktualizuj wartości filtrowania
def update_filter_options(app):
    statuses = sorted(set(m.status for m in app.manager.movies))
    genres = sorted(set(m.genre for m in app.manager.movies))
    directors = sorted(set(m.director for m in app.manager.movies))
    years = sorted(set(str(m.year) for m in app.manager.movies))

    app.status_cb['values'] = [""] + statuses
    app.genre_cb['values'] = [""] + genres
    app.director_cb['values'] = [""] + directors
    app.year_cb['values'] = [""] + years
