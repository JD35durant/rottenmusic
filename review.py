from datetime import datetime

class Review:
    def __init__(self, user, rating, comment):
        self.user = user
        self.rating = rating
        self.comment = comment
        self.date = datetime.now()
