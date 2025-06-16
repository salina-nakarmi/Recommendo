# Book Recommendation System

## Setup
1. Clone repo:
   `git clone https://github.com/salina-nakarmi/recommendo.git`
2. `python3 -m venv mendoenv`
3. `source mendoenv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `python app.py`


## 📘 Book Recommendation Dataset - Enhanced Version

This project uses the <a href="https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset" target="_blank">Book Recommendation Dataset</a> from Kaggle and enhances it by:
- Preprocessing the raw data (cleaning, merging, and filtering)
- Grouping users by age segments
- Extracting genres and descriptions using the Google Books API

---

## ✅ Use the Already Processed Dataset

You can directly use the processed file without running any preprocessing scripts:

📁 [data/final_processed.csv](./data/final_processed.csv)

This CSV includes:
- ISBN, Book Title, Author, Publisher
- Average Book Rating
- Rating Count (number of ratings received)
- Dominant Age Group of raters

---

## 🔧 How the Data Was Processed (If You Want to Recreate It)

### 1. Download Raw Data

Get the original dataset from Kaggle:  
👉 [Book Recommendation Dataset on Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

Extract and place the following files in the `data/raw/` directory:

