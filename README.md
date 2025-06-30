# Book Recommendation System

## Setup
```bash
git clone https://github.com/salina-nakarmi/recommendo.git
cd recommendo
python3 -m venv mendoenv

# Linux/Mac
source mendoenv/bin/activate

# Windows
.\mendoenv\Scripts\activate

pip install -r requirements.txt
python model/trainer.py
python app.py
```

##  Book Recommendation Dataset - Enhanced Version

This project uses the [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) from Kaggle and enhances it by:  
- Preprocessing the raw data (cleaning, merging, and filtering)
- Grouping users by age segments
- Extracting genres and descriptions using the Google Books API

---

##  Use the Already Processed Dataset

You can directly use the processed file without running any preprocessing scripts:

[final_processed.csv](https://drive.google.com/file/d/1oia6BrTSuEU4KX9UFMO7j5aZTWKC-jKj/view?usp=sharing)

you can store it under this 'data/final_processed.csv' 

The dataset was cleaned for the use of genre in frontend:
[clean_genre.csv](https://drive.google.com/file/d/18ChS5oIPcshihKHjZjleWvL31jKcE52g/view?usp=sharing)

you can store it under this 'data/clean_genre.csv' 

This CSV includes:
- ISBN, Book Title, Author, year of Publication, Publisher, Book-cover img
- Average Book Rating
- Rating Count (number of ratings received)
- Dominant Age Group of raters
- Genre
- Description

---

##  How the Data Was Processed (If You Want to Recreate It)

### 1. Download Raw Data

Get the original dataset from Kaggle:  
 [Book Recommendation Dataset on Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

Extract and place the following files in the `data/raw/` directory:
- Books.csv
- Users.csv
- Ratings.csv

#### Step 2: Run the Script

```bash
python book_rating_age.py
```

This script will:

- Merge datasets

- Clean and filter based on age and rating frequency

- Assign users into age groups

- Determine the dominant age group for each ISBN

- Export the result to data/processed/book_rating_age.csv

### 2. Genre + Description Extraction

After preprocessing, ~14,000 books were left.
We enriched them by fetching with batch processing:

- Genre

- Book Descriptions

Using Google Books API via Google Colab-[Genre and Description extractor](https://colab.research.google.com/drive/1DFBB740MgnWUP-pkftQ7G4rMxWIcTqBt?usp=sharing)

## Data Cleaning Code
-Using fuzzywuzzy via Google Collab- [Genre Data clean](https://colab.research.google.com/drive/16iOemQ2ZHeVKQzttHnXBbzkeNXUFAfp9?usp=sharing)
