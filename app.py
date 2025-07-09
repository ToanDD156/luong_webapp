from flask import Flask, render_template, request, redirect, session
import sqlite3

app = Flask(__name__)
app.secret_key = "supersecretkey"

def get_user(mnv, password):
    conn = sqlite3.connect("data.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT * FROM luong WHERE `Mã số`=? AND `Mật khẩu`=?", (mnv, password))
    row = cur.fetchone()
    conn.close()
    return row

@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        mnv = request.form["mnv"]
        pw = request.form["password"]
        user = get_user(mnv, pw)
        if user:
            session["user"] = dict(user)
            return redirect("/salary")
        else:
            error = "Sai mã NV hoặc mật khẩu"
    return render_template("login.html", error=error)

@app.route("/salary")
def salary():
    user = session.get("user")
    if not user:
        return redirect("/")
    return render_template("salary.html", user=user)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
