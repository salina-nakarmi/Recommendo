# File: batch_genre_extractor.py
# Processes books in 10-minute batches with progress saving

import pandas as pd
import requests
import time
import re
import os
from datetime import datetime, timedelta

class BatchGenreExtractor:
    def __init__(self, max_time_minutes=10):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'BookRecommendationSystem/1.0 (Educational Project)'
        })
        self.max_time_seconds = max_time_minutes * 60
        self.start_time = None
        
        # Genre mapping
        self.genre_mapping = {
            "Fiction": "Fiction", "Literary Fiction": "Fiction", "General Fiction": "Fiction",
            "Fantasy": "Fantasy", "Science Fiction": "Science Fiction", "Sci-Fi": "Science Fiction", "Urban Fantasy": "Fantasy",
            "Mystery": "Mystery", "Thriller": "Thriller", "Crime": "Mystery", "Detective": "Mystery",
            "Romance": "Romance", "Contemporary Romance": "Romance", "Historical Romance": "Romance",
            "Young Adult": "Young Adult", "YA Fiction": "Young Adult", "Teen": "Young Adult",
            "Biography": "Biography", "History": "History", "Self-Help": "Self-Help", "Business": "Business",
            "Health": "Health & Fitness", "Cooking": "Cooking", "Travel": "Travel",
            "Children's Books": "Children", "Juvenile Fiction": "Children", "Picture Books": "Children"
        }
    
    def time_remaining(self):
        """Check if we still have time left in this batch"""
        if not self.start_time:
            return True
        elapsed = time.time() - self.start_time
        return elapsed < self.max_time_seconds
    
    def clean_isbn(self, isbn):
        """Clean ISBN and make it API-ready"""
        if pd.isna(isbn) or isbn == '':
            return None
        isbn_clean = re.sub(r'[^0-9X]', '', str(isbn).upper())
        if len(isbn_clean) in [10, 13]:
            return isbn_clean
        return None
    
    def get_genre_from_openlibrary(self, isbn):
        """Fetch genre from OpenLibrary API"""
        try:
            url = f"https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data"
            response = self.session.get(url, timeout=3)  # Faster timeout for batches
            
            if response.status_code == 200:
                data = response.json()
                key = f"ISBN:{isbn}"
                
                if key in data and 'subjects' in data[key]:
                    subjects = data[key]['subjects']
                    genres = []
                    
                    for subject in subjects[:3]:
                        genre_name = subject.get('name', '')
                        standardized = self.standardize_genre(genre_name)
                        if standardized and standardized not in genres:
                            genres.append(standardized)
                    
                    return genres[:2]
            
            time.sleep(0.1)  # Quick rate limiting
            return []
            
        except Exception:
            return []
    
    def get_genre_from_google(self, isbn):
        """Fetch genre from Google Books API"""
        try:
            url = f"https://www.googleapis.com/books/v1/volumes?q=isbn:{isbn}"
            response = self.session.get(url, timeout=3)
            
            if response.status_code == 200:
                data = response.json()
                
                if data.get('totalItems', 0) > 0:
                    book_info = data['items'][0]['volumeInfo']
                    
                    if 'categories' in book_info:
                        genres = []
                        for category in book_info['categories'][:2]:
                            parts = category.split('/')
                            for part in parts:
                                standardized = self.standardize_genre(part.strip())
                                if standardized and standardized not in genres:
                                    genres.append(standardized)
                        
                        return genres[:2]
            
            time.sleep(0.05)  # Quick rate limiting
            return []
            
        except Exception:
            return []
    
    def standardize_genre(self, genre_text):
        """Standardize genre names"""
        if not genre_text:
            return None
        
        genre_text = genre_text.strip()
        
        if genre_text in self.genre_mapping:
            return self.genre_mapping[genre_text]
        
        for key, value in self.genre_mapping.items():
            if key.lower() in genre_text.lower():
                return value
        
        if len(genre_text) > 2 and genre_text.replace(' ', '').isalpha():
            return genre_text.title()
        
        return None
    
    def assign_fallback_genre(self, title, author):
        """Quick fallback genre assignment"""
        text = f"{title} {author}".lower()
        
        if any(word in text for word in ['mystery', 'detective', 'murder', 'crime']):
            return 'Mystery'
        elif any(word in text for word in ['romance', 'love']):
            return 'Romance'
        elif any(word in text for word in ['fantasy', 'magic', 'dragon']):
            return 'Fantasy'
        elif any(word in text for word in ['history', 'historical']):
            return 'History'
        elif any(word in text for word in ['child', 'kid']):
            return 'Children'
        else:
            return 'Fiction'
    
    def save_progress(self, df, batch_num, processed_count):
        """Save current progress"""
        progress_file = f"data/processed/Books_batch_{batch_num}_progress.csv"
        df.to_csv(progress_file, index=False)
        
        # Also save a summary
        summary = {
            'batch_number': batch_num,
            'processed_books': processed_count,
            'timestamp': datetime.now().isoformat(),
            'books_with_genres': sum(df['Genre'] != ''),
            'api_success': sum(df['Genre_Source'].isin(['openlibrary', 'google'])),
            'fallback_used': sum(df['Genre_Source'] == 'fallback')
        }
        
        summary_file = "data/processed/batch_progress_summary.txt"
        with open(summary_file, 'a') as f:
            f.write(f"Batch {batch_num}: {summary}\n")
        
        print(f"✅ Progress saved: {progress_file}")
        return progress_file
    
    def find_last_processed(self):
        """Find where we left off"""
        if not os.path.exists("data/processed"):
            return 0, None
        
        batch_files = [f for f in os.listdir("data/processed") if f.startswith("Books_batch_") and f.endswith("_progress.csv")]
        
        if not batch_files:
            return 0, None
        
        # Find highest batch number
        batch_numbers = []
        for f in batch_files:
            try:
                num = int(f.split('_')[2])
                batch_numbers.append(num)
            except:
                continue
        
        if batch_numbers:
            last_batch = max(batch_numbers)
            last_file = f"data/processed/Books_batch_{last_batch}_progress.csv"
            return last_batch, last_file
        
        return 0, None
    
    def process_batch(self, input_file, batch_size=None):
        """Process one batch of books for max 10 minutes"""
        self.start_time = time.time()
        
        print(f"🚀 Starting new batch (Max {self.max_time_seconds//60} minutes)")
        print(f"⏰ Started at: {datetime.now().strftime('%H:%M:%S')}")
        
        # Check for existing progress
        last_batch, last_file = self.find_last_processed()
        
        if last_file and os.path.exists(last_file):
            print(f"📁 Resuming from batch {last_batch}")
            df = pd.read_csv(last_file)
            start_idx = len(df[df['Genre'] != ''])  # Find where we stopped
            batch_num = last_batch + 1
        else:
            print(f"📖 Starting fresh from {input_file}")
            df = pd.read_csv(input_file)
            # Add genre columns if they don't exist
            if 'Genre' not in df.columns:
                df['Genre'] = ''
            if 'Genre_Source' not in df.columns:
                df['Genre_Source'] = ''
            start_idx = 0
            batch_num = 1
        
        total_books = len(df)
        processed_in_batch = 0
        api_success = 0
        fallback_used = 0
        
        print(f"📊 Total books: {total_books}")
        print(f"📍 Starting from index: {start_idx}")
        
        # Process books until time runs out
        for idx in range(start_idx, total_books):
            if not self.time_remaining():
                print(f"⏰ Time limit reached! Stopping batch.")
                break
            
            row = df.iloc[idx]
            
            # Skip if already processed
            if df.at[idx, 'Genre'] != '':
                continue
            
            isbn = self.clean_isbn(row['ISBN'])
            genres = []
            source = 'fallback'
            
            # Try APIs if ISBN is valid
            if isbn and self.time_remaining():
                genres = self.get_genre_from_openlibrary(isbn)
                if genres:
                    source = 'openlibrary'
                    api_success += 1
                elif self.time_remaining():
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
            
            # Update dataframe
            df.at[idx, 'Genre'] = genres[0] if genres else 'Unknown'
            df.at[idx, 'Genre_Source'] = source
            
            processed_in_batch += 1
            
            # Quick progress update
            if processed_in_batch % 10 == 0:
                elapsed = (time.time() - self.start_time) / 60
                print(f"⚡ Processed {processed_in_batch} | API: {api_success} | Fallback: {fallback_used} | Time: {elapsed:.1f}min")
        
        # Save progress
        progress_file = self.save_progress(df, batch_num, start_idx + processed_in_batch)
        
        # Final stats
        elapsed_time = (time.time() - self.start_time) / 60
        total_processed = sum(df['Genre'] != '')
        
        print(f"\n🎉 Batch {batch_num} Complete!")
        print(f"⏱️  Time taken: {elapsed_time:.1f} minutes")
        print(f"📈 Processed in this batch: {processed_in_batch}")
        print(f"📊 Total processed so far: {total_processed}/{total_books} ({total_processed/total_books*100:.1f}%)")
        print(f"🎯 API success rate: {api_success}/{processed_in_batch} ({api_success/processed_in_batch*100:.1f}%)" if processed_in_batch > 0 else "")
        
        # Show next steps
        if total_processed < total_books:
            remaining = total_books - total_processed
            estimated_batches = remaining // processed_in_batch if processed_in_batch > 0 else remaining // 100
            print(f"📋 Remaining: {remaining} books (~{estimated_batches} more batches)")
            print(f"💡 Run again to continue: python batch_genre_extractor.py")
        else:
            print(f"🏆 ALL DONE! Creating final dataset...")
            final_file = "data/processed/Books_with_genres_FINAL.csv"
            df.to_csv(final_file, index=False)
            print(f"📁 Final dataset: {final_file}")
        
        return df

def main():
    """Run batch processing"""
    print("🔧 10-Minute Batch Genre Extractor")
    print("=" * 50)
    
    input_file = "data/raw/Books.csv"
    
    if not os.path.exists(input_file):
        print(f"❌ File not found: {input_file}")
        return
    
    os.makedirs("data/processed", exist_ok=True)
    
    extractor = BatchGenreExtractor(max_time_minutes=10)
    extractor.process_batch(input_file)

if __name__ == "__main__":
    main()