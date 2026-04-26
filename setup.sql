-- ============================================
-- MusicDB - 
-- ============================================

CREATE DATABASE musicdb CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE musicdb;

-- ============================================
-- TABLE : users
-- ============================================
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    password_hash VARCHAR(255) NOT NULL
);

-- ============================================
-- TABLE : artists
-- ============================================
CREATE TABLE artists (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    genre VARCHAR(100),
    image_url VARCHAR(500)
);

-- ============================================
-- TABLE : albums
-- ============================================
CREATE TABLE albums (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    year INT,
    genre VARCHAR(100),
    image_url VARCHAR(500),
    CONSTRAINT fk_album_artist
        FOREIGN KEY (artist_id)
        REFERENCES artists(id)
        ON DELETE CASCADE
);

-- ============================================
-- TABLE : songs
-- ============================================
CREATE TABLE songs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    artist_id INT NOT NULL,
    duration VARCHAR(10),
    image_url VARCHAR(500),
    CONSTRAINT fk_song_artist
        FOREIGN KEY (artist_id)
        REFERENCES artists(id)
        ON DELETE CASCADE
);

-- ============================================
-- TABLE : reviews
-- ============================================
CREATE TABLE reviews (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    item_type ENUM('artist','album','song') NOT NULL,
    item_id INT NOT NULL,
    rating INT NOT NULL CHECK (rating BETWEEN 1 AND 10),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_review_user
        FOREIGN KEY (user_id)
        REFERENCES users(id)
        ON DELETE CASCADE
);

