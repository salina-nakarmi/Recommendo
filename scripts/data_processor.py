# This runs ONCE to process your data, not every time the app starts

import pandas as pd
import numpy as np
import pickle
import os
from pathlib import Path

class BookDataProcessor:
    def __init__(self, data_dir="data"):
        self.data_dir = Path(data_dir)
        self.raw_dir = self.data_dir / "raw"
        self.processed_dir = self.data_dir / "processed"
        self.models_dir = self.data_dir / "models"
        
        # Create directories if they don't exist
        for dir_path in [self.processed_dir, self.models_dir]:
            dir_path.mkdir(parents=True, exist_ok=True)
    
    def load_raw_data(self):
        """Load the original CSV files"""
        print("Loading raw data...")
        self.books_df = pd.read_csv(self.raw_dir / "Books.csv")
        self.ratings_df = pd.read_csv(self.raw_dir / "Ratings.csv") 
        self.users_df = pd.read_csv(self.raw_dir / "Users.csv")
        
        print(f"Loaded {len(self.books_df)} books")
        print(f"Loaded {len(self.ratings_df)} ratings")
        print(f"Loaded {len(self.users_df)} users")
    
    def clean_books_data(self):
        """Clean the books dataset"""
        print("Cleaning books data...")
        
        # Create a copy
        books_clean = self.books_df.copy()
        
        # Remove duplicates and missing data
        books_clean = books_clean.drop_duplicates(subset=['ISBN'])
        books_clean = books_clean.dropna(subset=['ISBN', 'Book-Title', 'Book-Author'])
        
        # Clean publication years
        books_clean = books_clean[
            (books_clean['Year-Of-Publication'] >= 1000) & 
            (books_clean['Year-Of-Publication'] <= 2025)
        ]
        
        # Fill missing publishers
        books_clean['Publisher'] = books_clean['Publisher'].fillna('Unknown Publisher')
        
        self.books_clean = books_clean
        print(f"Cleaned dataset: {len(books_clean)} books")
    
    def extract_genres(self):
        """Extract genres from titles and publishers - ADD NEW COLUMN"""
        print("Extracting genres...")
        
        def extract_genre_from_text(title, publisher=""):
            """Extract genre hints from title and publisher text"""
            text = (str(title) + " " + str(publisher)).lower()
            
            genre_patterns = {
                'romance': ['romance', 'love', 'heart', 'passion', 'wedding', 'bride'],
                'mystery': ['mystery', 'murder', 'detective', 'crime', 'killer', 'death'],
                'fantasy': ['fantasy', 'magic', 'dragon', 'wizard', 'kingdom', 'sword'],
                'sci-fi': ['science', 'space', 'future', 'robot', 'alien', 'galaxy'],
                'horror': ['horror', 'ghost', 'vampire', 'demon', 'dark', 'nightmare'],
                'children': ['children', 'kids', 'young', 'junior', 'elementary'],
                'history': ['history', 'historical', 'war', 'ancient', 'century'],
                'biography': ['biography', 'autobiography', 'memoir', 'life'],
                'business': ['business', 'management', 'success', 'money', 'finance'],
                'health': ['health', 'diet', 'fitness', 'medical', 'wellness'],
                'religion': ['god', 'bible', 'christian', 'religious', 'spiritual'],
                'cooking': ['cook', 'recipe', 'kitchen', 'food', 'chef'],
                'travel': ['travel', 'guide', 'country', 'city', 'journey']
            }
            
            detected_genres = []
            for genre, keywords in genre_patterns.items():
                if any(keyword in text for keyword in keywords):
                    detected_genres.append(genre)
            
            return detected_genres if detected_genres else ['general']
        
        # ADD NEW COLUMNS for genres
        self.books_clean['genres'] = self.books_clean.apply(
            lambda row: extract_genre_from_text(row['Book-Title'], row['Publisher']), 
            axis=1
        )
        
        # Primary genre (first detected genre)
        self.books_clean['primary_genre'] = self.books_clean['genres'].apply(
            lambda x: x[0] if x else 'general'
        )
        
        print("Genre extraction completed!")
        
        # Show genre distribution
        all_genres = []
        for genre_list in self.books_clean['genres']:
            all_genres.extend(genre_list)
        
        genre_counts = pd.Series(all_genres).value_counts()
        print("Top genres found:")
        print(genre_counts.head(10))
    
    def create_features(self):
        """Create additional features for recommendations"""
        print("Creating features...")
        
        # Publication era
        def categorize_year(year):
            if year < 1950: return 'Classic'
            elif year < 1980: return 'Retro'
            elif year < 2000: return 'Modern'
            else: return 'Contemporary'
        
        self.books_clean['era'] = self.books_clean['Year-Of-Publication'].apply(categorize_year)
        
        # Author productivity
        author_counts = self.books_clean['Book-Author'].value_counts()
        self.books_clean['author_book_count'] = self.books_clean['Book-Author'].map(author_counts)
        self.books_clean['is_prolific_author'] = self.books_clean['author_book_count'] >= 5
        
        print("Feature creation completed!")
    
    def save_processed_data(self):
        """Save all processed datasets"""
        print("Saving processed data...")
        
        # Save the main processed dataset
        self.books_clean.to_csv(self.processed_dir / "books_processed.csv", index=False)
        
        # Save a lightweight version for the web app
        web_columns = [
            'ISBN', 'Book-Title', 'Book-Author', 'Year-Of-Publication', 
            'Publisher', 'primary_genre', 'genres', 'era', 'author_book_count'
        ]
        
        web_dataset = self.books_clean[web_columns].copy()
        web_dataset.to_csv(self.processed_dir / "books_for_web.csv", index=False)
        
        print("Data saved successfully!")
    
    def process_all(self):
        """Run the complete processing pipeline"""
        print("=== STARTING DATA PROCESSING PIPELINE ===")
        
        self.load_raw_data()
        self.clean_books_data()
        self.extract_genres()
        self.create_features()
        self.save_processed_data()
        
        print("=== PROCESSING COMPLETE ===")
        print(f"Final dataset: {len(self.books_clean)} books")
        print(f"Files saved in: {self.processed_dir}")

# RUN THIS ONCE - STANDALONE SCRIPT
if __name__ == "__main__":
    processor = BookDataProcessor()
    processor.process_all()