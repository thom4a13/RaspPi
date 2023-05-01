from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route("/")
def index():
    conn = sqlite3.connect('dht11.db')
    c = conn.cursor()
    c.execute("SELECT * FROM readings ORDER BY id DESC LIMIT 1") # get the latest data from the database
    latest_data = c.fetchone()
    conn.close()
    return render_template("index.html", temperature=latest_data[2], humidity=latest_data[3])

if __name__ == "__main__":
    app.run(debug=True)
