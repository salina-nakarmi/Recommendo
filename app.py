from flask import Flask, render_template , request, flash, redirect, url_for
from genre_load import load_dataset, get_unique_genre
import os
import subprocess

app = Flask(__name__)
app.secret_key = 'dev'

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


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/searchbook', methods=['GET', 'POST'])
def book():
    if request.method == 'POST':
        print(f"Total books in dataset: {len(df)}")  # Debug line
        print(f"Sample books: {df['Book-Title'].head()}")  # Debug line
        book_name = request.form.get('query', '').strip()
        if not book_name:
            flash("Please enter a book name to search.", 'error')
            return render_template('recommend.html', books=None)

        try:
            recommended_isbns = recommend_books(book_name)
            
            if not recommended_isbns:
                flash(f"No recommendations found for '{book_name}'. Try another title.", 'error')
                return render_template('recommend.html', books=[], search_query=book_name)

            books = df[df['ISBN'].isin(recommended_isbns)].to_dict(orient='records')

            # Try to find the exact match if available
            exact_match = df[df['Book-Title'].str.lower() == book_name.lower()]
            if not exact_match.empty:
                searched_isbn = exact_match.iloc[0]['ISBN']
                books.sort(key=lambda b: 0 if b['ISBN'] == searched_isbn else 1)
            else:
                flash(f"Exact match not found for '{book_name}', showing similar books.", 'info')

            return render_template('recommend.html', books=books, search_query=book_name)

        except Exception as e:
            flash(f"An error occurred while searching for books: {str(e)}", 'error')
            return render_template('recommend.html', books=[], search_query=book_name)

    return render_template('recommend.html', books=None)


@app.route('/book/<isbn>')
def show_book(isbn):
    try:
        book_row = df[df['ISBN'] == isbn]
        if book_row.empty:
            flash("Book not found.", 'error')
            return redirect(url_for('book'))
            
        book_name = book_row.iloc[0]['Book-Title']
        recommended_isbns = recommend_books(book_name)
        
        if not recommended_isbns:
            flash(f"No recommendations found for '{book_name}'.", 'info')
            return render_template('info.html', books=[book_row.to_dict(orient='records')[0]])

        books = df[df['ISBN'].isin(recommended_isbns)].to_dict(orient='records')
        books.sort(key=lambda b: 0 if b['ISBN'] == isbn else 1)
        
        return render_template('info.html', books=books)

    except Exception as e:
        flash(f"An error occurred: {str(e)}", 'error')
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(debug=True)
