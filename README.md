# Book Recommendation System

## Setup
1. Clone repo:
   `git clone https://github.com/salina-nakarmi/recommendo.git`
2. `python3 -m venv mendoenv`
3. `source mendoenv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `python app.py`


## 📘 Book Recommendation Dataset - Enhanced Version

This project uses the This project uses the [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) from Kaggle and enhances it by:  
- Preprocessing the raw data (cleaning, merging, and filtering)
- Grouping users by age segments
- Extracting genres and descriptions using the Google Books API

---

## ✅ Use the Already Processed Dataset

You can directly use the processed file without running any preprocessing scripts:

[final_processed.csv](https://drive.google.com/file/d/1oia6BrTSuEU4KX9UFMO7j5aZTWKC-jKj/view?usp=sharing)

'data/final_processed.csv' you can store it under this file.

This CSV includes:
- ISBN, Book Title, Author, year of Publication, Publisher, Book-cover img
- Average Book Rating
- Rating Count (number of ratings received)
- Dominant Age Group of raters
- Genre
- Description

---

## 🔧 How the Data Was Processed (If You Want to Recreate It)

### 1. Download Raw Data

Get the original dataset from Kaggle:  
👉 [Book Recommendation Dataset on Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

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

Using Google Books API via Google Colab-[genre and description extractor](https://colab.research.google.com/drive/1yDquOOx65x_G-aTTZhtWl2W6ANQOlcFQ?usp=sharing)


