from abc import ABC, abstractmethod
from core.review import Review

class MediaItem(ABC):
    def __init__(self, id, name, image_url=None):
        self.id = id
        self.name = name
        self.image_url = image_url or "/static/images/no-image.png"
        self.reviews = []

    def add_review(self, user, rating, comment):
        self.reviews.append(Review(user, rating, comment))

    def get_average_rating(self):
        if not self.reviews:
            return 0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @abstractmethod
    def get_type(self):
        pass

    @abstractmethod
    def display_info(self):
        pass
