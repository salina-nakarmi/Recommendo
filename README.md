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
python app.py
```

##  Book Recommendation Dataset - Enhanced Version

This project uses the [Book Recommendation Dataset](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset) from Kaggle and enhances it by:  
- Preprocessing the raw data (cleaning, merging, and filtering)
- Extracting genres and descriptions using the Google Books API

---

##  Use the Already Processed Dataset

You can directly use the processed file without running any preprocessing scripts:

[final_processed.csv](https://drive.google.com/file/d/1oia6BrTSuEU4KX9UFMO7j5aZTWKC-jKj/view?usp=sharing)

you can store it under this 'data/final_processed.csv' 

We also have done EDA of the data- [EDA](https://github.com/salina-nakarmi/Recommendo/blob/main/EDA.ipynb)

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
As the genres in the dataset needed cleaning due to
- genre being characters names
- morphological variants (fiction, fictions, fictional, etc..)
  
So to remove them fuzzy matching was applied.
- Using fuzzywuzzy via Google Collab- [Genre Data clean](https://colab.research.google.com/drive/16iOemQ2ZHeVKQzttHnXBbzkeNXUFAfp9?usp=sharing)

## Model Building – Content-Based Book Recommendation
We built a Content-Based Recommendation System that suggests books similar to a given title using the cosine similarity of their textual features.

Key Steps:

#### 1. Data Selection:
 We selected only the necessary columns from the dataset:
 "Book-Title", "Book-Author","Publisher", "Genre", "Description"
 and removed rows with missing values and duplicates based on book titles.


#### 2. Feature Engineering:
 A new column called Combined_feature was created by merging key textual information such as title, author, publisher, genre, and description into a single string. Then it was converted to lowercase. This forms the input text for vectorization.


#### 3. Vectorization with TF-IDF:
 We used TfidfVectorizer from scikit-learn to convert the combined text features into numerical vectors while removing common English stop words.


#### 4. Similarity Computation:
 Pairwise cosine similarity was calculated using the cosine_similarity function from scikit-learn. This gives us a similarity score between every pair of books.


#### 5. Recommendation Function:
 A function recommend_books(title) was created to return the top n(5 in our case) most similar books  based on cosine similarity scores.
