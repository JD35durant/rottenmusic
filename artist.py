from core.media_item import MediaItem

class Artist(MediaItem):
    def __init__(self, id, name, genre, image_url=None):
        super().__init__(id, name, image_url)
        self.genre = genre

    def get_type(self):
        return "artist"

    def display_info(self):
        return f"Artiste : {self.name} ({self.genre})"
