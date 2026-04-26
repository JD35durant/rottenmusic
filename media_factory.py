from repositories.artist_repo import ArtistRepository
from repositories.album_repo import AlbumRepository
from repositories.song_repo import SongRepository
from repositories.review_repo import ReviewRepository

class MediaFactory:
    @staticmethod
    def load(item_type, item_id):
        if item_type == "artist":
            item = ArtistRepository.get(item_id)
        elif item_type == "album":
            item = AlbumRepository.get(item_id)
        elif item_type == "song":
            item = SongRepository.get(item_id)
        else:
            raise Exception("Type inconnu")

        item.reviews = ReviewRepository.get_reviews(item_type, item_id)
        return item
