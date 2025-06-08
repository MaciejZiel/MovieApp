from tkinter import Toplevel, Text, Scrollbar, Button, Frame
# Pokazuje okno z informacjami wybranego filmu
def show_details(app):
    selected_items = app.tree.selection()
    if not selected_items:
        return
    item_id = selected_items[0]
    index = app.tree.index(item_id)
    movie = app.filtered_movies[index]
    app.selected_index = index

    # Tworzenie informacji ze szczegółami filmu
    details_text = (
        f"Tytuł: {movie.title}\n"
        f"Reżyser: {movie.director}\n"
        f"Rok: {movie.year}\n"
        f"Gatunek: {movie.genre}\n"
        f"Status: {movie.status}\n"
        f"Ocena: {movie.rating}\n"
        f"Opis: {movie.description}\n"
        f"Data obejrzenia: {movie.watch_date}\n"
    )

    if movie.comments:
        details_text += "\nKomentarze:\n"
        for c in movie.comments:
            details_text += f"- {c}\n"

    # Tworzenie nowego okna z tekstem
    details_window = Toplevel(app.root)
    details_window.title("Szczegóły filmu")

    frame = Frame(details_window)
    frame.pack(padx=10, pady=10, fill="both", expand=True)

    text_widget = Text(frame, wrap="word", width=50, height=15)
    text_widget.pack(side="left", fill="both", expand=True)
    text_widget.insert("1.0", details_text)
    text_widget.config(state="disabled")

    scrollbar = Scrollbar(frame, orient="vertical", command=text_widget.yview)
    scrollbar.pack(side="right", fill="y")
    text_widget.config(yscrollcommand=scrollbar.set)

    close_button = Button(details_window, text="Zamknij", command=details_window.destroy)
    close_button.pack(pady=(0, 10))

# Ładuje dane filmu do obiektu
def load_movie_into_fields(app, movie):
    app.title_var.set(movie.title)
    app.director_var.set(movie.director)
    app.year_var.set(str(movie.year))
    app.genre_var.set(movie.genre)
    app.status_var.set(movie.status)
    app.rating_var.set(str(movie.rating))
    app.desc_var.set(movie.description)
