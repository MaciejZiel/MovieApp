from tkinter import ttk

def setup_ui(app):
    # Główna ramka
    frm = ttk.Frame(app.root)
    frm.pack(padx=10, pady=10, fill="both", expand=True)

    # Etykiety
    labels = ["Tytuł", "Reżyser", "Rok", "Gatunek", "Status", "Ocena", "Opis"]
    for i, text in enumerate(labels):
        ttk.Label(frm, text=text).grid(row=i, column=0, sticky="w", pady=2)

    # Pola wejściowe
    for i, var in enumerate(app.vars):
        if i == 4:
            cb = ttk.Combobox(frm, textvariable=var, values=["Obejrzany", "Do obejrzenia"], state="readonly")
            cb.grid(row=i, column=1, sticky="ew", pady=2)
            if not var.get():
                var.set("Do obejrzenia")
        elif i == 6:
            ttk.Entry(frm, textvariable=var, width=50).grid(row=i, column=1, sticky="ew", pady=2)
        else:
            ttk.Entry(frm, textvariable=var).grid(row=i, column=1, sticky="ew", pady=2)

    frm.columnconfigure(1, weight=1)

    # Przyciskowe akcje pod polami
    btn_frame = ttk.Frame(frm)
    btn_frame.grid(row=7, column=0, columnspan=2, pady=10)
    ttk.Button(btn_frame, text="Dodaj", command=app.add_movie).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Edytuj", command=app.edit_movie).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Usuń", command=app.delete_movie).pack(side="left", padx=5)
    ttk.Button(btn_frame, text="Wyczyść pola", command=app.clear_fields).pack(side="left", padx=5)

    #Filtrowanie
    filter_frame = ttk.LabelFrame(app.root, text="Filtry")
    filter_frame.pack(fill="x", padx=10, pady=5)

    ttk.Label(filter_frame, text="Tytuł:").grid(row=0, column=0, sticky="w", pady=2)
    ttk.Entry(filter_frame, textvariable=app.search_var).grid(row=0, column=1, sticky="ew", pady=2)

    ttk.Label(filter_frame, text="Status:").grid(row=0, column=2, sticky="w", pady=2)
    app.status_cb = ttk.Combobox(filter_frame, textvariable=app.filter_status, state="readonly")
    app.status_cb.grid(row=0, column=3, sticky="ew", pady=2)

    ttk.Label(filter_frame, text="Gatunek:").grid(row=1, column=0, sticky="w", pady=2)
    app.genre_cb = ttk.Combobox(filter_frame, textvariable=app.filter_genre, state="readonly")
    app.genre_cb.grid(row=1, column=1, sticky="ew", pady=2)

    ttk.Label(filter_frame, text="Reżyser:").grid(row=1, column=2, sticky="w", pady=2)
    app.director_cb = ttk.Combobox(filter_frame, textvariable=app.filter_director, state="readonly")
    app.director_cb.grid(row=1, column=3, sticky="ew", pady=2)

    ttk.Label(filter_frame, text="Rok:").grid(row=2, column=0, sticky="w", pady=2)
    app.year_cb = ttk.Combobox(filter_frame, textvariable=app.filter_year, state="readonly")
    app.year_cb.grid(row=2, column=1, sticky="ew", pady=2)

    # Przycisk filtrowania i resetu
    ttk.Button(filter_frame, text="Filtruj", command=app.apply_filters).grid(row=2, column=2, sticky="ew", pady=2)
    ttk.Button(filter_frame, text="Resetuj filtry", command=app.reset_filters).grid(row=2, column=3, sticky="ew", pady=2)

    for i in range(4):
        filter_frame.columnconfigure(i, weight=1)

    # Tabela z listą filmów
    columns = ("Tytuł", "Rok", "Gatunek", "Status", "Ocena")
    app.tree = ttk.Treeview(app.root, columns=columns, show="headings", selectmode="browse")
    for col in columns:
        app.tree.heading(col, text=col, command=lambda c=col: app.sort_by_column(c))
        app.tree.column(col, minwidth=50, width=100)
    app.tree.pack(fill="both", expand=True, padx=10, pady=10)
    app.tree.bind("<<TreeviewSelect>>", app.on_tree_select)

    # Dodatkowe przyciski pod tabelą
    add_info_frame = ttk.LabelFrame(app.root, text="Dodatkowe informacje")
    add_info_frame.pack(fill="x", padx=10, pady=5)

    ttk.Button(add_info_frame, text="Generuj Wykresy", command=app.generate_charts).grid(row=0, column=0, pady=2)
    ttk.Button(add_info_frame, text="Więcej szczegółów", command=app.show_details).grid(row=0, column=2, pady=2, padx=10)
    ttk.Button(add_info_frame, text="Dodaj komentarz", command=app.add_comment_popup_external).grid(row=0, column=3, pady=2, padx=10)
    ttk.Button(add_info_frame, text="Eksportuj dane", command=app.export_movies_to_txt).grid(row=0, column=4, pady=2, padx=10)
