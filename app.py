from flask import Flask, render_template , request

app = Flask(__name__)

@app.route('/')
def home():
    books = [
        {"title": "The Hobbit", "author": "J.R.R. Tolkien"},
        {"title": "Dune", "author": "Frank Herbert"}
    ]
    return render_template('index.html', books=books)

@app.route('/genre')
def genre():
    return render_template('chooseGenre.html')

@app.route("/searchbook", methods= ["GET", "POST"])
def book():
    return render_template("recommend.html")




if __name__ == '__main__':
    app.run(debug=True)