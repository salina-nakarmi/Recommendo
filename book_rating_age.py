import pandas as pd
import os
from pathlib import Path


"""
    Preprocesses book rating data by combining ratings, user age information,
    and filtering based on rating frequency.
    
    Returns:
        pd.DataFrame: Final processed dataframe with ISBN, ratings, and user age info
"""
print("Starting data preprocessing...")

# Load raw data
print("Loading raw data files...")
books = pd.read_csv('data/raw/Books.csv')
ratings = pd.read_csv('data/raw/Ratings.csv')
users = pd.read_csv('data/raw/Users.csv')
        
print(f"Loaded {len(books)} books, {len(ratings)} ratings, {len(users)} users")
        
# Display basic info about ratings
print(f"\nRatings dataframe info:")
print(f"Columns: {list(ratings.columns)}")
print(f"Shape: {ratings.shape}")
        
# Count unique ISBNs
rated_isbns_count = ratings['ISBN'].nunique()
print(f"\nNumber of unique ISBNs that have been rated: {rated_isbns_count}")
        
# Calculate average rating for each ISBN
print("Calculating average ratings per ISBN...")
average_ratings = ratings.groupby('ISBN')['Book-Rating'].mean().round(2).reset_index(name='Average-Book-Rating')
print(f"Average ratings shape: {average_ratings.shape}")
        
# Count rating frequency for each ISBN
print("Calculating rating frequency per ISBN...")
user_frequency = ratings.groupby('ISBN').size().reset_index(name='Rating-Count')
        
# Merge average ratings with frequency
average_ratings = pd.merge(average_ratings, user_frequency, on='ISBN')
print(f"Merged ratings shape: {average_ratings.shape}")
        
# Filter to keep top 24000 books by rating count
print("Filtering books by rating frequency...")
average_ratings_sorted = average_ratings.sort_values('Rating-Count', ascending=False)
average_ratings_filtered = average_ratings_sorted.iloc[:24000]
print(f"Filtered ratings shape: {average_ratings_filtered.shape}")
        
# Prepare user age data
print("Processing user age data...")
users_age = users[['Age', 'User-ID']]
        
# Merge ratings with user age
ratings_with_age = pd.merge(ratings, users_age, on='User-ID', how='inner')
print(f"Ratings with age shape: {ratings_with_age.shape}")
        
# Filter ratings by the selected ISBNs
filtered_isbns = average_ratings_filtered['ISBN'].tolist()
ratings_filtered_by_isbn_with_age = ratings_with_age[
    ratings_with_age['ISBN'].isin(filtered_isbns)
]
print(f"Filtered ratings with age shape: {ratings_filtered_by_isbn_with_age.shape}")
        
# Calculate average user age per ISBN
print("Calculating average user age per ISBN...")
average_age_per_filtered_isbn = ratings_filtered_by_isbn_with_age.groupby('ISBN')['Age'].mean().round(2).reset_index(name='Av-User-Age')
        
# Create final merged dataframe
print("rating_age")
rating_age = pd.merge(
    average_ratings_filtered, 
    average_age_per_filtered_isbn, 
    on='ISBN', 
    how='left'
)
        
print("book_rating_age")
book_rating_age = pd.merge(
    books,
    rating_age,
    on='ISBN',
    how='inner'
)
print(f"\nFinal processed dataframe:")
print(f"Columns: {list(book_rating_age.columns)}")
print(f"Shape: {book_rating_age.shape}")
print(f"Sample data:")
print(book_rating_age.head())
        
# Save processed data
print(f"\nSaving processed data to {'data/processed/'}...")
book_rating_age.to_csv('data/processed/book_rating_age.csv', index=False)
print("Data preprocessing completed successfully!")
        



