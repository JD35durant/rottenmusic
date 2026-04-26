from core.media_item import MediaItem

class Album(MediaItem):
    def __init__(self, id, title, artist, year, genre, image_url=None):
        super().__init__(id, title, image_url)
        self.artist = artist
        self.year = year
        self.genre = genre

    def get_type(self):
        return "album"

    def display_info(self):
        return f"Album : {self.name} ({self.year})"
