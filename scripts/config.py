# File: scripts/config.py

# Configuration for genre extraction
API_CONFIG = {
    "google_books": {
        "base_url": "https://www.googleapis.com/books/v1/volumes",
        "rate_limit": 0.1,  # seconds between requests
        "timeout": 10
    },
    "openlibrary": {
        "base_url": "https://openlibrary.org/api/books",
        "rate_limit": 0.2,
        "timeout": 10
    }
}

# Genre mapping to standardize genre names
GENRE_MAPPING = {
    # Fiction genres
    "Fiction": "Fiction",
    "Literary Fiction": "Fiction",
    "General Fiction": "Fiction",
    
    # Fantasy & Sci-Fi
    "Fantasy": "Fantasy",
    "Science Fiction": "Science Fiction",
    "Sci-Fi": "Science Fiction",
    "Urban Fantasy": "Fantasy",
    
    # Mystery & Thriller
    "Mystery": "Mystery",
    "Thriller": "Thriller",
    "Crime": "Mystery",
    "Detective": "Mystery",
    
    # Romance
    "Romance": "Romance",
    "Contemporary Romance": "Romance",
    "Historical Romance": "Romance",
    
    # Young Adult
    "Young Adult": "Young Adult",
    "YA Fiction": "Young Adult",
    "Teen": "Young Adult",
    
    # Non-Fiction
    "Biography": "Biography",
    "History": "History",
    "Self-Help": "Self-Help",
    "Business": "Business",
    "Health": "Health & Fitness",
    "Cooking": "Cooking",
    "Travel": "Travel",
    
    # Children's
    "Children's Books": "Children",
    "Juvenile Fiction": "Children",
    "Picture Books": "Children"
}

# Fallback genres for books without API data
FALLBACK_GENRES = [
    "Fiction", "Non-Fiction", "Mystery", "Romance", "Fantasy", 
    "Science Fiction", "Biography", "History", "Self-Help", "Children"
]