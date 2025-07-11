from flask import Flask, render_template , request
from genre_load import load_dataset, get_unique_genre
import os
import subprocess

app = Flask(__name__)

def run_trainer_if_needed():
    pkl_dir = './model/pkl'
    if not os.path.exists(pkl_dir) or not os.listdir(pkl_dir):
        print("[INFO] Trained data missing. Running trainer...")
        subprocess.run(['python', './model/trainer.py'], check=True)

run_trainer_if_needed()


from model.engine import recommend_books

df = load_dataset()
unique_genres = get_unique_genre(df)

@app.route('/')
def home():
  
    def get_books_by_genre(genre_name):
        filtered = df[df['Genre'].str.contains(genre_name, case=False, na=False)]
        return filtered.sample(n=5, replace=False).to_dict(orient='records') if len(filtered) >= 5 else filtered.to_dict(orient='records')

    fiction_books = get_books_by_genre('Fiction')
    juvenile_books = get_books_by_genre('Juvenile Fiction')
    biography_books = get_books_by_genre('Biography & Autobiography')
    business_books = get_books_by_genre('Business & Economics')

    return render_template('index.html',
                           fiction_books=fiction_books,
                           juvenile_books=juvenile_books,
                           biography_books=biography_books,
                           business_books=business_books)


@app.route('/choose_genre')
def genre():
    return render_template('chooseGenre.html', genres=unique_genres)

@app.route('/searchbook', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        book_name = request.form.get('query', '').strip()
        if not book_name:
            flash("Please enter a book name to search.")
            return render_template('recommend.html', books=None)

        recommended_isbns = recommend_books(book_name)

        if not recommended_isbns:
            flash(f"No recommendations found for '{book_name}'. Try another title.")
            return render_template('recommend.html', books=[])

        books = df[df['ISBN'].isin(recommended_isbns)].to_dict(orient='records')

        searched_isbn = recommended_isbns[0]
        books.sort(key=lambda b: 0 if b['ISBN'] == searched_isbn else 1)

        return render_template('recommend.html', books=books)

    return render_template('recommend.html', books=None)


@app.route('/book/<isbn>')
def show_book(isbn):
    book_row = df[df['ISBN'] == isbn]
    if book_row.empty:
        flash("Book not found.")
        return render_template('info.html', books=[])

    book_name = book_row.iloc[0]['Book-Title']

    recommended_isbns = recommend_books(book_name)

    books = df[df['ISBN'].isin(recommended_isbns)].to_dict(orient='records')
    books.sort(key=lambda b: 0 if b['ISBN'] == isbn else 1)

    return render_template('info.html', books=books)



if __name__ == '__main__':
    app.run(debug=True)
