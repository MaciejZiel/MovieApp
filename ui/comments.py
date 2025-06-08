from tkinter import messagebox, Toplevel, Label, Entry, Button
# Dodaj komentarz do aktualnie zaznaczonego filmu
def add_comment_to_movie(app, comment):
    if not comment.strip():
        messagebox.showwarning("Pusty komentarz", "Komentarz nie może być pusty.")
        return

    if app.selected_index is None:
        messagebox.showwarning("Brak filmu", "Wybierz film.")
        return

    movie = app.filtered_movies[app.selected_index]
    movie.comments.append(comment.strip())
    app.manager.save()
    messagebox.showinfo("Sukces", "Komentarz dodany.")

# Wyświetla okno do dodania komentarza
def add_comment_popup(app, movie):
    comment_window = Toplevel(app.root)
    comment_window.title("Dodaj komentarz")

    Label(comment_window, text="Treść komentarza:").pack(pady=(10, 0))
    comment_entry = Entry(comment_window, width=50)
    comment_entry.pack(pady=(0, 10))

    def save_and_close():
        add_comment_to_movie(app, comment_entry.get())
        comment_window.destroy()

    Button(comment_window, text="Dodaj", command=save_and_close).pack()

def add_comment_popup_external(app):
    if app.selected_index is None:
        messagebox.showwarning("Brak filmu", "Wybierz film z listy.")
        return
    movie = app.filtered_movies[app.selected_index]
    add_comment_popup(app, movie)
