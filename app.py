from cs50 import SQL
from flask import Flask, render_template, session, request, redirect, url_for, jsonify
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import messages, login_required, fetch, list_add, gamelist, list_remove, list_update, global_best_rated, my_best_rated, game_data, change_password
import requests
from math import ceil
from credentials import CLIENT_ID, ACCESS_TOKEN

app = Flask(__name__)

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"

Session(app)

db = SQL("sqlite:///games.db")

CLIENT_ID = CLIENT_ID
ACCESS_TOKEN = ACCESS_TOKEN
IGDB_URL = "https://api.igdb.com/v4/games/"



@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    """Home Page"""

    userId = session['user_id']
    username = session['username']

    #GET
    if request.method == "GET":
        code = request.args.get("code")
        return render_template("index.html", message=messages(code), globalbestrated=global_best_rated(), mybestrated=my_best_rated(), username=session['username'])
    
    #POST
    return render_template("index.html")


@app.route("/mylist", methods=["GET", "POST"])
@login_required
def mylist():

    #GET
    if request.method == "GET":
        games = gamelist()
        code = request.args.get("code")
        return render_template("mylist.html", games=games, message=messages(code), username=session['username']) 

    #POST
    gameId = request.form.get("gameId")
    action = request.form.get("action")
    if action == "remove":
        code = list_remove(gameId)

    return redirect(url_for("mylist", code=code))


@app.route("/global_chart")
@login_required
def global_chart():
    index = request.args.get("index")
    if not index:
        index = 0
    else:
        index = int(index) * 10
    

    games = global_best_rated()
    pages = len(games)/10
    pages = ceil(pages)
     
    return render_template("global_chart.html", globalBestRated=games, index=index, pages=pages, username=session['username'])




@app.route("/game", methods=["GET", "POST"])
@login_required
def game():
    """Render page with the game"""

    #GET
    if request.method == "GET":
        query = request.args.getlist("query")
        action = request.args.get("action")
        game = game_data(query)
        if not game:
            return "Game not found"
        code = request.args.get("code")
        return render_template("game.html", game=game, message=messages(code), action=action, username=session['username'])
    
    #POST
    gameId = request.form.get("gameId")
    status = request.form.get("status")
    if status == "toplay":
        code = list_add(gameId, status, None, None)
    elif not status:
        code = 19
    else:
        rating = request.form.get("rating")
        if not rating or not rating.isdigit() or int(rating) < 0 or int(rating) > 10:
            code = 18
        else:
            commentary = request.form.get("commentary", "No comments")
            code = list_add(gameId, status, rating, commentary)

    return redirect(url_for("game", query=gameId, code=code))


@app.route("/search")
@login_required
def search():

    #GET
    if request.method == "GET":
        query = request.args.getlist("query")
        games = fetch(query, "name")
        return render_template("search.html", games=games, username=session['username'], query=query[0])


@app.route("/settings", methods=["GET", "POST"])
@login_required
def settings():
    """Account management"""

    #GET
    if request.method == "GET":
        code = request.args.get("code")
        return render_template("settings.html", username=session['username'], message=messages(code))
    
    #POST
    oldPassword = request.form.get("oldPassword")
    newPassword = request.form.get("newPassword")

    if oldPassword == newPassword:
        code = 24
    elif not newPassword:
        code = 3
    elif not oldPassword:
        code = 1
    else:
        code = change_password(oldPassword, newPassword)

    return redirect(url_for("settings", code=code))


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()

    #GET
    if request.method == "GET":
        code = request.args.get("code")
        if code:
            return render_template("login.html", message=messages(code))
        return render_template("login.html")
    
    #POST
    username = request.form.get("username")
    password = request.form.get("password")
    rows = db.execute("SELECT * FROM users WHERE username = ?", username)

    #validation
    if not username:
        return redirect(url_for("login", code=0))
    if not password:
        return redirect(url_for("login", code=1))
    if not rows or not check_password_hash(rows[0]["hash"], password):
        return redirect(url_for("login", code=2))
    
    #feeding session information
    userId = rows[0]["id"]
    session['user_id'] = userId
    session['username'] = username

    return redirect(url_for("index"))


@app.route("/api/searchbar", methods=["GET","POST"])
def api_searchbar():

    query = request.args.get("query")

    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": ACCESS_TOKEN,
    }

    data = f'fields name, release_dates.y, cover.image_id, genres.name; where name ~ *"{query}"*; limit 3; sort rating_count desc;'

    response = requests.post(IGDB_URL, headers=headers, data=data)

    if response.status_code == 200:
        return jsonify(response.json())
    elif response.status_code == 429:
        return response.status_code
    else:
        return jsonify({"error": "failed to fetch data", "code":  response.status_code})


@app.route("/register", methods=["GET", "POST"])
def register():

    #GET
    if request.method == "GET":
        code = request.args.get("code")
        if code:
            return render_template("register.html", message=messages(code))
        return render_template("register.html", message="")
    
    #POST
    username = request.form.get("username")
    password = request.form.get("password")
    passwordConfirm = request.form.get("passwordConfirm")

    #validation
    if not username:
        return redirect(url_for("register", code=0))
    if not password:
        return redirect(url_for("register", code=1))
    if not passwordConfirm:
        return redirect(url_for("register", code=3))
    if not passwordConfirm == password:
        return redirect(url_for("register", code=4))
    rows = db.execute("SELECT username FROM users WHERE username = ?", username)
    if rows:
        return redirect(url_for("register", code=5))
    
    db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, generate_password_hash(password))
    
    return redirect(url_for("index"))


@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    """Log user out"""
    session.clear()
    return redirect(url_for("login"))


    
    

