class Movie:
    def __init__(self, title, director, year, genre, status, rating, description, comments=None,watch_date= None):
        self.title = title
        self.director = director
        self.year = year
        self.genre = genre
        self.status = status
        self.rating = rating
        self.description = description
        self.comments = comments if comments is not None else []
        self.watch_date = watch_date

    def to_dict(self):
        return self.__dict__
