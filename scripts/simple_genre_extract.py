# File: scripts/simple_genre_extract.py

import pandas as pd
import requests
import time
import re
from config import GENRE_MAPPING, FALLBACK_GENRES

class SimpleGenreExtractor:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BookRecommendationSystem/1.0 (Educational Project)'
        })
    
    def clean_isbn(self, isbn):
        """Clean ISBN and make it API-ready"""
        if pd.isna(isbn) or isbn == '':
            return None
        
        # Convert to string and remove any non-alphanumeric characters
        isbn_clean = re.sub(r'[^0-9X]', '', str(isbn).upper())
        
        # Basic ISBN validation
        if len(isbn_clean) in [10, 13]:
            return isbn_clean
        return None
    
    def get_genre_from_openlibrary(self, isbn):
        """Fetch genre from OpenLibrary API"""
        try:
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                key = f"ISBN:{isbn}"
                
                if key in data and 'subjects' in data[key]:
                    subjects = data[key]['subjects']
                    genres = []
                    
                    for subject in subjects[:5]:  # First 5 subjects
                        genre_name = subject.get('name', '')
                        standardized = self.standardize_genre(genre_name)
                        if standardized and standardized not in genres:
                            genres.append(standardized)
                    
                    return genres[:2]  # Return max 2 genres
            
            time.sleep(0.2)  # Rate limiting
            return []
            
        except Exception as e:
            print(f"Error with OpenLibrary for ISBN {isbn}: {e}")
            return []
    
    def get_genre_from_google(self, isbn):
        """Fetch genre from Google Books API"""
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = self.session.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('totalItems', 0) > 0:
                    book_info = data['items'][0]['volumeInfo']
                    
                    if 'categories' in book_info:
                        genres = []
                        for category in book_info['categories'][:3]:
                            # Handle compound categories like "Fiction / Romance"
                            parts = category.split('/')
                            for part in parts:
                                standardized = self.standardize_genre(part.strip())
                                if standardized and standardized not in genres:
                                    genres.append(standardized)
                        
                        return genres[:2]  # Return max 2 genres
            
            time.sleep(0.1)  # Rate limiting
            return []
            
        except Exception as e:
            print(f"Error with Google Books for ISBN {isbn}: {e}")
            return []
    
    def standardize_genre(self, genre_text):
        """Standardize genre names using mapping"""
        if not genre_text:
            return None
        
        genre_text = genre_text.strip()
        
        # Direct mapping
        if genre_text in GENRE_MAPPING:
            return GENRE_MAPPING[genre_text]
        
        # Partial matching for compound genres
        for key, value in GENRE_MAPPING.items():
            if key.lower() in genre_text.lower():
                return value
        
        # If no mapping found, return cleaned original
        if len(genre_text) > 2 and genre_text.replace(' ', '').isalpha():
            return genre_text.title()
        
        return None
    
    def assign_fallback_genre(self, title, author):
        """Assign fallback genre based on title/author keywords"""
        text = f"{title} {author}".lower()
        
        # Simple keyword-based assignment
        if any(word in text for word in ['mystery', 'detective', 'murder', 'crime']):
            return 'Mystery'
        elif any(word in text for word in ['romance', 'love', 'heart']):
            return 'Romance'
        elif any(word in text for word in ['fantasy', 'magic', 'dragon', 'wizard']):
            return 'Fantasy'
        elif any(word in text for word in ['history', 'historical', 'war', 'ancient']):
            return 'History'
        elif any(word in text for word in ['child', 'kid', 'young']):
            return 'Children'
        else:
            return 'Fiction'  # Default fallback
    
    def process_books_simple(self, input_file, output_file=None):
        """Process books with simple genre extraction"""
        print(f"Loading {input_file}...")
        df = pd.read_csv(input_file)
        
        # Add genre columns
        df['Genre'] = ''
        df['Genre_Source'] = ''  # Track where genre came from
        
        total_books = len(df)
        processed = 0
        api_success = 0
        fallback_used = 0
        
        print(f"Processing {total_books} books...")
        
        for idx, row in df.iterrows():
            isbn = self.clean_isbn(row['ISBN'])
            genres = []
            source = 'fallback'
            
            # Try APIs if ISBN is valid
            if isbn:
                # Try OpenLibrary first (more reliable for genres)
                genres = self.get_genre_from_openlibrary(isbn)
                if genres:
                    source = 'openlibrary'
                    api_success += 1
                else:
                    # Try Google Books as backup
                    genres = self.get_genre_from_google(isbn)
                    if genres:
                        source = 'google'
                        api_success += 1
            
            # Use fallback if no API success
            if not genres:
                fallback_genre = self.assign_fallback_genre(
                    row.get('Book-Title', ''), 
                    row.get('Book-Author', '')
                )
                genres = [fallback_genre]
                fallback_used += 1
            
            # Assign to dataframe
            df.at[idx, 'Genre'] = genres[0] if genres else 'Unknown'
            df.at[idx, 'Genre_Source'] = source
            
            processed += 1
            
            # Progress update
            if processed % 25 == 0:
                print(f"Processed {processed}/{total_books} | API Success: {api_success} | Fallback: {fallback_used}")
        
        # Final statistics
        print(f"\n=== Processing Complete ===")
        print(f"Total books: {total_books}")
        print(f"API success: {api_success} ({api_success/total_books*100:.1f}%)")
        print(f"Fallback used: {fallback_used} ({fallback_used/total_books*100:.1f}%)")
        
        # Save results
        if output_file is None:
            output_file = input_file.replace('.csv', '_with_genres.csv')
        
        df.to_csv(output_file, index=False)
        print(f"Saved to: {output_file}")
        
        # Show genre distribution
        print(f"\nGenre Distribution:")
        print(df['Genre'].value_counts().head(10))
        
        return df

# Usage example
if __name__ == "__main__":
    extractor = SimpleGenreExtractor()
    
    # Process your books
    input_path = "data/raw/Books.csv"
    output_path = "data/processed/Books_with_genres.csv"
    
    try:
        result_df = extractor.process_books_simple(input_path, output_path)
        print("\nGenre extraction completed successfully!")
        
    except FileNotFoundError:
        print(f"File not found: {input_path}")
        print("Make sure your Books.csv is in the correct location.")
    except Exception as e:
        print(f"Error: {e}")