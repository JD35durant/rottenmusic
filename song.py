from core.media_item import MediaItem

class Song(MediaItem):
    def __init__(self, id, title, artist, duration, image_url=None):
        super().__init__(id, title, image_url)
        self.artist = artist
        self.duration = duration

    def get_type(self):
        return "song"

    def display_info(self):
        return f"Chanson : {self.name} ({self.duration})"
