from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def home():
    books = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
        {"title": "Dune", "author": "Frank Herbert"}
    ]
    return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)