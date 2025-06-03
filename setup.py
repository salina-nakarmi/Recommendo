# setup.py - Run this ONCE to set up your data
import os
from pathlib import Path

def create_directory_structure():
    """Create the recommended directory structure"""
    directories = [
        "data/raw",
        "data/processed", 
        "data/models",
        "scripts",
        "utils"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"Created directory: {directory}")

def move_csv_files():
    """Move CSV files to data/raw/ if they're in the root"""
    csv_files = ["Books.csv", "Ratings.csv", "Users.csv"]
    
    for csv_file in csv_files:
        if Path(csv_file).exists():
            destination = Path("data/raw") / csv_file
            if not destination.exists():
                Path(csv_file).rename(destination)
                print(f"Moved {csv_file} to data/raw/")
            else:
                print(f"{csv_file} already exists in data/raw/")
        else:
            print(f"WARNING: {csv_file} not found in root directory")

def create_init_files():
    """Create __init__.py files for Python packages"""
    init_files = ["scripts/__init__.py", "utils/__init__.py"]
    
    for init_file in init_files:
        Path(init_file).touch()
        print(f"Created {init_file}")

def create_gitignore():
    """Create .gitignore to exclude data files"""
    gitignore_content = """
# Data files
data/raw/*.csv
data/processed/*.csv
data/models/*.pkl

# Python
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db
"""
    
    with open(".gitignore", "w") as f:
        f.write(gitignore_content.strip())
    print("Created .gitignore")

def main():
    print("=== SETTING UP RECOMMENDO PROJECT ===")
    
    create_directory_structure()
    move_csv_files()
    create_init_files()
    create_gitignore()
    
    print("\n=== SETUP COMPLETE ===")
    print("Next steps:")
    print("1. Make sure your CSV files are in data/raw/")
    print("2. Run: python scripts/data_processor.py")
    print("3. Run: python app.py")

if __name__ == "__main__":
    main()