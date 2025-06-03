import pandas as pd

df = pd.read_csv("data/raw/Books.csv")
# STEP 1: First look at your data
print("=== BASIC DATA INFO ===")
print(f"Dataset shape: {df.shape}")
print(f"Columns: {list(df.columns)}")
print("\n=== FIRST FEW ROWS ===")
print(df.head())

print("\n=== DATA TYPES ===") 
print(df.dtypes)

print("\n=== MISSING VALUES ===")
print(df.isnull().sum())

print("\n=== BASIC STATISTICS ===")
print(df.describe())
