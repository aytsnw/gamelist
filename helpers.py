from cs50 import SQL
from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from functools import wraps
from werkzeug.security import generate_password_hash, check_password_hash
import requests
from time import sleep


CLIENT_ID = "2f110wt67l4ofxl9kxo6guwn7qzopi"
ACCESS_TOKEN = "Bearer f2xgr58udy518f4mxac4lktizykwq1"
IGDB_URL = "https://api.igdb.com/v4/games/"

db = SQL("sqlite:///games.db")


def messages(code):
    """Returns common error messages"""
    messages = {"0":"Must provide username", "1":"Must provide password",
            "2":"Invalid username or password", "3":"Must provide password confirmation",
            "4":"Passwords don't match", "5":"Username already exists","6":"Invalid username",
            "7":"Invite sent!", "8":"User already invited", "9":"No ongoing adventures",
            "10": "Game already added to list!", "11": "Game added to list!", "12": "Game removed from your list",
            "13": "Couldn't delete user from your list, try again", "14": "Status updated!", "15": "Couldn't update game status",
            "16": "You must login first!", "17":"Couldn't add game to list, try again", "18": "Must select a valid rating",
            "19": "Must select a status", "20":"Password changed!", "21": "Couldn't change password, try again!",
            "22": "Wrong current password!", "23": "Password changed!", "24": "Passwords can't be equal!"}
    
    return messages.get(code, "")

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (f.__name__ == "game" or f.__name__ == "search" or f.__name__ =="mylist") and not session.get('user_id'):
            return redirect(url_for("login", code=16))
        elif not session.get('user_id'):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return decorated_function

def fetch(list, field, column="unknown"):

    data = f'fields id, name, summary, artworks.url, genres.name, release_dates.human, screenshots.image_id, cover.image_id;'
    length = len(list)

    if field == "name":
        data += f' where name ~ *"{list[0]}"*; sort rating_count desc;'
    
    elif field == "id":
        data += f' where id = ({list[0][column]}'
        if not length == 1:
            for i in range(1, length):
                data += f',{list[i][column]}'
        data += '); limit 15;'


    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": ACCESS_TOKEN,
    }


    response = requests.post(IGDB_URL, headers=headers, data=data)

    if response.status_code == 200:
        response = response.json()
        return response
    else:
        return None
    
def game_data(gameId_list):
    gameId = gameId_list[0]
    list = [{"id": gameId}]
    game = fetch(list, "id", column="id")

    rows = db.execute("SELECT * FROM user_games WHERE game_id = ?", gameId)
    if not rows:
        return game[0]
    
    commentaries = []
    rows = db.execute("SELECT * FROM user_games JOIN users ON user_games.user_id = users.id WHERE game_id = ? AND user_id = ?", gameId, session['user_id'])
    
    for i in range(len(rows)):
        commentaries.append({"commentary": rows[i]["commentary"], "username": rows[i]["username"]})

    rows2 = db.execute("SELECT rating, rating_count FROM games WHERE id = ?", gameId)

    game[0]["commentaries"] = commentaries
    game[0]["rating"] = rows2[0]["rating"]
    game[0]["rating_count"] = rows2[0]["rating_count"]

    if not rows:
        return game[0]
    
    game[0]["user_rating"] = rows[0]["rating"]
    game[0]["user_commentary"] = rows[0]["commentary"]

    return game[0]

    

def list_add(gameId, status, rating, commentary):

    rows = db.execute("SELECT * FROM user_games WHERE user_id = ? AND game_id = ?", session["user_id"], gameId)
    if rows:
        list_remove(gameId)

    if db.execute("INSERT INTO user_games (user_id, game_id, status, rating, commentary) VALUES(?, ?, ?, ?, ?)", session['user_id'], gameId, status, rating, commentary):
        rows2 = db.execute("SELECT * FROM games WHERE id = ?", gameId)
        if not rows2:
            if db.execute("INSERT INTO games (id, rating, rating_count) VALUES(?, ?, ?)", gameId, rating, 1):
                return 11
            return 17
        elif db.execute("UPDATE games SET rating_count = rating_count + 1, rating = (SELECT AVG(rating) FROM user_games WHERE game_id = ?) WHERE id = ?", gameId, gameId):
            return 11
        return 17
    
    return 17

    
    

def list_remove(gameId):
    if db.execute("DELETE FROM user_games WHERE game_id = ? AND user_id = ?", gameId, session['user_id']):
        if db.execute("UPDATE games SET rating_count = rating_count - 1, rating = (SELECT AVG(rating) FROM user_games WHERE game_id = ?) WHERE id = ?", gameId, gameId):
            if db.execute("DELETE FROM games WHERE rating_count = 0"):
                return 12
    
    return 13

def list_update(gameId, status):
    if db.execute("UPDATE user_games SET status = ? WHERE game_id = ? AND user_id = ?", status, gameId, session["user_id"]):
        return 14
    
    return 15

def gamelist():
    rows = db.execute("SELECT * FROM user_games WHERE user_id = ?", session['user_id'])
    if not rows:
        return None
    
    response = fetch(rows, "id", "game_id")
    games = []
    i = 0
    
    for item in rows:
        for game in response:
            if game["id"] == item["game_id"]:
                game["status"] = rows[i]["status"]
                game["rating"] = rows[i]["rating"]
                game["commentary"] = rows[i]["commentary"]
                games.append(game)
                i += 1

    return games

def global_best_rated():
    rows = db.execute("SELECT * FROM games ORDER BY rating DESC")
    if not rows:
        return None
    
    response = fetch(rows, "id", "id")
    games = []
    i = 0

    for item in rows:
        for game in response:
            if game["id"] == item["id"]:
                games.append(game)
                games[i]["rating"] = item["rating"]
                games[i]["rating_count"] = item["rating_count"]
                games[i]["index"] = i  
                i += 1

    return games   

def my_best_rated():
    rows = db.execute("SELECT * FROM user_games WHERE user_id = ? ORDER BY rating DESC", session['user_id'])
    if not rows:
        return None
    
    response = fetch(rows, "id", "game_id")
    games = []
    i = 0

    for item in rows:
        for game in response:
            if game["id"] == item["game_id"]:
                game["rating"] = item["rating"]
                game["commentary"] = item["commentary"]
                games.append(game)     
                i += 1   
    return games  

def change_password(oldPassword, newPassword):
    rows = db.execute("SELECT hash FROM users WHERE id = ?", session['user_id'])
    if not rows:
        return 21
    
    if not check_password_hash(rows[0]["hash"], oldPassword):
        return 22
    
    if db.execute("UPDATE users SET hash = ? WHERE id = ?", generate_password_hash(newPassword), session['user_id']):
        return 23
    
    return 21




    









        

    






     
    
