# File: run_genre_extraction.py
# Place this in your project root directory

import os
import sys
import pandas as pd

# Add scripts directory to path
sys.path.append('scripts')

def check_files():
    """Check if required files exist"""
    books_file = "data/raw/Books.csv"
    
    if not os.path.exists(books_file):
        print(f"❌ File not found: {books_file}")
        print("Please make sure your Books.csv file is in the data/raw/ directory")
        return False
    
    print(f"✅ Found: {books_file}")
    
    # Create processed directory if it doesn't exist
    os.makedirs("data/processed", exist_ok=True)
    
    return True

def preview_data():
    """Preview the current data structure"""
    try:
        df = pd.read_csv("data/raw/Books.csv")
        print(f"\n📊 Current Data Overview:")
        print(f"Total books: {len(df)}")
        print(f"Columns: {list(df.columns)}")
        print(f"\nFirst few rows:")
        print(df.head(2))
        
        # Check for existing genre columns
        genre_cols = [col for col in df.columns if 'genre' in col.lower()]
        if genre_cols:
            print(f"\n⚠️  Found existing genre columns: {genre_cols}")
            print("The script will update these columns.")
        
        return True
    except Exception as e:
        print(f"❌ Error reading Books.csv: {e}")
        return False

def main():
    print("🔧 Book Genre Extraction Setup")
    print("=" * 40)
    
    # Check files
    if not check_files():
        return
    
    # Preview data
    if not preview_data():
        return
    
    print(f"\n🚀 Ready to extract genres!")
    print(f"This will:")
    print(f"  1. Add 'Genre' and 'Genre_Source' columns to your Books.csv")
    print(f"  2. Use ISBN to fetch genres from book APIs")
    print(f"  3. Use smart fallbacks for books without API data")
    print(f"  4. Save results to data/processed/Books_with_genres.csv")
    
    response = input(f"\nProceed with genre extraction? (y/n): ").lower().strip()
    
    if response == 'y':
        try:
            # Import and run the extraction
            from simple_genre_extract import SimpleGenreExtractor
            
            extractor = SimpleGenreExtractor()
            result_df = extractor.process_books_simple(
                "data/raw/Books.csv",
                "data/processed/Books_with_genres.csv"
            )
            
            print(f"\n🎉 Success! Your books now have genres.")
            print(f"📁 Check the file: data/processed/Books_with_genres.csv")
            
        except ImportError:
            print(f"❌ Could not import extraction scripts.")
            print(f"Make sure config.py and simple_genre_extract.py are in the scripts/ directory")
        except Exception as e:
            print(f"❌ Error during extraction: {e}")
    else:
        print(f"👋 Cancelled. Run this script again when ready.")

if __name__ == "__main__":
    main()