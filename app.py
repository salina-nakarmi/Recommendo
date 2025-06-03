# app.py - Your main Flask application
# This LOADS pre-processed data, doesn't process it every time

from flask import Flask, render_template, request, jsonify
import pandas as pd
from pathlib import Path
import os

app = Flask(__name__)

# Global variable to store data (loaded once when app starts)
books_data = None

def load_processed_data():
    """Load the pre-processed data when the app starts"""
    global books_data
    
    data_path = Path("data/processed/books_for_web.csv")
    
    if data_path.exists():
        print("Loading processed book data...")
        books_data = pd.read_csv(data_path)
        print(f"Loaded {len(books_data)} books")
        
        # Convert string representation of lists back to actual lists
        books_data['genres'] = books_data['genres'].apply(eval)
        
        return True
    else:
        print("ERROR: Processed data not found!")
        print("Please run the data processing script first:")
        print("python scripts/data_processor.py")
        return False

def get_recommendations_by_genre(genre, limit=10):
    """Simple genre-based recommendations"""
    if books_data is None:
        return []
    
    # Filter books by genre
    genre_books = books_data[books_data['primary_genre'] == genre]
    
    if len(genre_books) == 0:
        return []
    
    # Sort by author popularity and recent publication
    recommendations = genre_books.sort_values(
        ['author_book_count', 'Year-Of-Publication'], 
        ascending=[False, False]
    ).head(limit)
    
    return recommendations.to_dict('records')

def get_books_by_author(author_name, limit=10):
    """Get books by specific author"""
    if books_data is None:
        return []
    
    author_books = books_data[
        books_data['Book-Author'].str.contains(author_name, case=False, na=False)
    ]
    
    return author_books.head(limit).to_dict('records')

@app.route('/')
def index():
    """Home page"""
    if books_data is None:
        return render_template('error.html', 
                             message="Data not loaded. Please process the data first.")
    
    # Get some stats for the homepage
    total_books = len(books_data)
    total_authors = books_data['Book-Author'].nunique()
    genres = books_data['primary_genre'].value_counts().head(10).to_dict()
    
    return render_template('index.html', 
                         total_books=total_books,
                         total_authors=total_authors,
                         top_genres=genres)

@app.route('/recommend')
def recommend():
    """Recommendations page"""
    return render_template('recommend.html')

@app.route('/api/recommend', methods=['POST'])
def api_recommend():
    """API endpoint for recommendations"""
    data = request.get_json()
    genre = data.get('genre', 'general')
    limit = data.get('limit', 10)
    
    recommendations = get_recommendations_by_genre(genre, limit)
    
    return jsonify({
        'success': True,
        'genre': genre,
        'count': len(recommendations),
        'books': recommendations
    })

@app.route('/api/search', methods=['POST'])
def api_search():
    """API endpoint for author search"""
    data = request.get_json()
    author = data.get('author', '')
    
    if not author:
        return jsonify({'success': False, 'message': 'Author name required'})
    
    books = get_books_by_author(author)
    
    return jsonify({
        'success': True,
        'author': author,
        'count': len(books),
        'books': books
    })

@app.route('/api/stats')
def api_stats():
    """API endpoint for dataset statistics"""
    if books_data is None:
        return jsonify({'success': False, 'message': 'Data not loaded'})
    
    stats = {
        'total_books': len(books_data),
        'total_authors': books_data['Book-Author'].nunique(),
        'total_publishers': books_data['Publisher'].nunique(),
        'year_range': {
            'min': int(books_data['Year-Of-Publication'].min()),
            'max': int(books_data['Year-Of-Publication'].max())
        },
        'genre_distribution': books_data['primary_genre'].value_counts().head(15).to_dict(),
        'era_distribution': books_data['era'].value_counts().to_dict()
    }
    
    return jsonify({'success': True, 'stats': stats})

# Initialize data when the app starts
@app.before_first_request
def initialize():
    """Load data before handling the first request"""
    success = load_processed_data()
    if not success:
        print("WARNING: App started without processed data!")

if __name__ == '__main__':
    # Try to load data immediately for development
    load_processed_data()
    app.run(debug=True)