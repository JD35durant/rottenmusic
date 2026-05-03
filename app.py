import os
import pymysql
from flask import Flask, render_template, request, redirect, session, jsonify

# Imports corrigés (fichiers à la racine)
import user_repo as UserRepository
import artist_repo as ArtistRepository  
import album_repo as AlbumRepository
import review_repo as ReviewRepository
import auth_service as AuthService
import ranking_service as RankingService
import image_service as ImageService
import media_factory as MediaFactory
import media_item as MediaItem
import db as db_module

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'SUPER_SECRET_KEY')

# Pour la fonction get_db, utilisez db_module.get_db
def get_db():
    return db_module.get_db()

# ... le reste de votre code
