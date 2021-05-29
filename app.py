
from flask import Flask, render_template, request
from game import game

app = Flask(__name__)

@app.route('/', methods=["GET","POST"])
def index():
    score= None
    if request.method == "POST":
        score = game()
    return render_template("index.html", score=score)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")