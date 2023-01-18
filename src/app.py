from flask import Flask, render_template, request, session, redirect, url_for
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)

# Datenbank mit Benutzern und Passwörtern
users = {
    "admin": "password",
    "user1": "password1",
    "user2": "password2"
}

# Blog-Einträge
blog_entries = [
    {"title": "Eintrag 1", "content": "Inhalt des ersten Eintrags"},
    {"title": "Eintrag 2", "content": "Inhalt des zweiten Eintrags"},
    {"title": "Eintrag 3", "content": "Inhalt des dritten Eintrags"}
]

# Login-Seite
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Prüfe ob Benutzername und Passwort in der Datenbank existieren
        if request.form["username"] in users and users[request.form["username"]] == request.form["password"]:
            session["username"] = request.form["username"]
            return redirect(url_for("index"))
        else:
            return "Falscher Benutzername oder Passwort"
    return render_template("login.html")

# Abmelden
@app.route("/logout")
def logout():
    session.pop("username", None)
    return redirect(url_for("index"))

# Blog-Startseite
@app.route("/")
def index():
    if "username" in session:
        return render_template("index.html", username=session["username"], blog_entries=blog_entries)
    return redirect(url_for("login"))

# Einzelner Blog-Eintrag
@app.route("/entries/<int:id>")
def entry(id):
    if "username" in session:
        return render_template("entry.html", entry=blog_entries[id])
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host='0.0.0.0')
