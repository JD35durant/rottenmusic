import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import requests
from io import BytesIO

from services.ranking_service import RankingService
from repositories.artist_repo import ArtistRepository

GENRES = ["rock", "pop", "rap", "jazz", "electro"]


# =========================
# SCROLLABLE FRAME
# =========================
class ScrollableFrame(ttk.Frame):
    def __init__(self, container):
        super().__init__(container)

        canvas = tk.Canvas(self, bg="#f4f4f4", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        self.scrollable_frame = ttk.Frame(canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        canvas.bind_all(
            "<MouseWheel>",
            lambda e: canvas.yview_scroll(-1 * (e.delta // 120), "units")
        )


# =========================
# MAIN APP
# =========================
class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Music App – Desktop")
        self.root.geometry("1200x800")
        self.root.configure(bg="#f4f4f4")

        self.images = []

        # =========================
        # HEADER
        # =========================
        header = tk.Frame(root, bg="#1e1e1e")
        header.pack(fill="x")

        tk.Label(
            header,
            text="🎵 Music App",
            font=("Segoe UI", 22, "bold"),
            fg="white",
            bg="#1e1e1e"
        ).pack(pady=(10, 2))

        tk.Label(
            header,
            text="Découverte musicale – Version Desktop",
            font=("Segoe UI", 10),
            fg="#bbbbbb",
            bg="#1e1e1e"
        ).pack(pady=(0, 10))

        # =========================
        # NAVIGATION
        # =========================
        nav = tk.Frame(root, bg="#eaeaea")
        nav.pack(fill="x", pady=2)

        tk.Button(nav, text="Accueil", width=12, command=self.show_home)\
            .pack(side="left", padx=5, pady=5)

        tk.Button(nav, text="Top Artistes", width=12, command=self.load_artists)\
            .pack(side="left", padx=5)

        tk.Button(nav, text="Top Albums", width=12, command=self.load_albums)\
            .pack(side="left", padx=5)

        self.genre_var = tk.StringVar(value="rock")
        ttk.Combobox(
            nav,
            textvariable=self.genre_var,
            values=GENRES,
            state="readonly",
            width=10
        ).pack(side="right", padx=10)

        self.search_var = tk.StringVar()
        tk.Entry(nav, textvariable=self.search_var, width=25)\
            .pack(side="right", padx=5)

        tk.Button(nav, text="Rechercher", command=self.search_artists)\
            .pack(side="right", padx=5)

        # =========================
        # CONTENT
        # =========================
        self.container = ScrollableFrame(root)
        self.container.pack(fill="both", expand=True, padx=10, pady=10)

        self.show_home()

    # =========================
    # UTILS
    # =========================
    def clear_content(self):
        for w in self.container.scrollable_frame.winfo_children():
            w.destroy()
        self.images.clear()

    def load_image(self, url, size=(200, 200)):
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            r = requests.get(url, headers=headers, timeout=10)
            r.raise_for_status()
            img = Image.open(BytesIO(r.content)).convert("RGB")
            img = img.resize(size)
            photo = ImageTk.PhotoImage(img)
            self.images.append(photo)
            return photo
        except Exception:
            return None

    # =========================
    # HOME PAGE (INDEX.HTML)
    # =========================
    def show_home(self):
        self.clear_content()
        frame = self.container.scrollable_frame

        # ---------- ARTISTES ----------
        tk.Label(
            frame,
            text="Artistes",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f4f4"
        ).pack(anchor="w", padx=10, pady=(10, 5))

        artists = RankingService.get_home_artists()

        artists_frame = tk.Frame(frame, bg="#f4f4f4")
        artists_frame.pack(fill="x")

        for i, artist in enumerate(artists):
            self.artist_card(artists_frame, artist, i)

        # ---------- ALBUMS ----------
        tk.Label(
            frame,
            text="Albums",
            font=("Segoe UI", 18, "bold"),
            bg="#f4f4f4"
        ).pack(anchor="w", padx=10, pady=(20, 5))

        albums = RankingService.get_home_albums()

        albums_frame = tk.Frame(frame, bg="#f4f4f4")
        albums_frame.pack(fill="x")

        for i, album in enumerate(albums):
            self.album_card(albums_frame, album, i)

    # =========================
    # CARDS
    # =========================
    def artist_card(self, parent, artist, index):
        card = tk.Frame(parent, bg="white", relief="groove", borderwidth=1)
        card.grid(row=index // 4, column=index % 4, padx=10, pady=10)
        card.configure(width=230, height=300)
        card.pack_propagate(False)

        img = self.load_image(artist["image_url"])
        if img:
            tk.Label(card, image=img, bg="white").pack()

        tk.Label(
            card,
            text=artist["name"],
            font=("Segoe UI", 10, "bold"),
            bg="white",
            wraplength=200
        ).pack(pady=4)

        tk.Label(
            card,
            text=artist["genre"],
            font=("Segoe UI", 9),
            bg="white",
            fg="#666"
        ).pack()

    def album_card(self, parent, album, index):
        card = tk.Frame(parent, bg="white", relief="groove", borderwidth=1)
        card.grid(row=index // 4, column=index % 4, padx=10, pady=10)
        card.configure(width=230, height=300)
        card.pack_propagate(False)

        img = self.load_image(album["image_url"])
        if img:
            tk.Label(card, image=img, bg="white").pack()

        tk.Label(
            card,
            text=album["title"],
            font=("Segoe UI", 10, "bold"),
            bg="white",
            wraplength=200
        ).pack(pady=4)

        tk.Label(
            card,
            text=album["genre"],
            font=("Segoe UI", 9),
            bg="white",
            fg="#666"
        ).pack()

    # =========================
    # TOPS & SEARCH
    # =========================
    def load_artists(self):
        self.clear_content()
        genre = self.genre_var.get()
        artists = RankingService.top10_artists_by_genre(genre)
        for i, artist in enumerate(artists):
            self.artist_card(self.container.scrollable_frame, artist, i)

    def load_albums(self):
        self.clear_content()
        genre = self.genre_var.get()
        albums = RankingService.top10_albums_by_genre(genre)
        for i, album in enumerate(albums):
            self.album_card(self.container.scrollable_frame, album, i)

    def search_artists(self):
        self.clear_content()
        results = ArtistRepository.search(self.search_var.get())
        for i, artist in enumerate(results):
            self.artist_card(self.container.scrollable_frame, artist, i)


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()