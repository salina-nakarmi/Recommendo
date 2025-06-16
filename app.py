from flask import Flask, render_template , request
from genre_load import load_dataset, get_unique_genre

app = Flask(__name__)

df = load_dataset()
unique_genres = get_unique_genre(df)

@app.route('/')
def home():
    books = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
        {"title": "Dune", "author": "Frank Herbert"}
    ]
    return render_template('index.html', books=books)

@app.route('/choose_genre')
def genre():
    return render_template('chooseGenre.html', genres=unique_genres)

@app.route("/searchbook", methods= ["GET", "POST"])
def book():
    return render_template("recommend.html")




if __name__ == '__main__':
    app.run(debug=True)