# Book Recommendation System

## Setup
1. Clone repo:
   `git clone https://github.com/salina-nakarmi/recommendo.git`
2. `python3 -m venv mendoenv`
3. `source mendoenv/bin/activate` (or `venv\Scripts\activate` on Windows)
4. `pip install -r requirements.txt`
5. `python app.py`


## Datasetup and Execution
1. **Download Dataset**

   Download the dataset from Kaggle:  
   👉 [Book Recommendation Dataset on Kaggle](https://www.kaggle.com/datasets/arashnic/book-recommendation-dataset)

2. **Organize Files**

After downloading, extract and place the following 3 CSV files into the `data/raw/` directory of this repository:

- `Users.csv`
- `Books.csv`
- `Ratings.csv`

3. **Run the Script**

Once the data is in place, run the script below to begin analysis:

```bash
python book_rating_age.py
