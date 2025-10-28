# book-scraper-python

## P2: Use Python basics for market analysis

This Python project was completed as part of Project 2 of the **Python Application Developer** path at OpenClassrooms.

It implements a web scraping program to extract pricing data and detailed information from the fictional bookstore Books to Scrape. The data is then structured and exported as **CSV** files.

## ⚙️ Scraper Features

The main.py program allows extracting data from https://books.toscrape.com/index.html and saving detailed information (title, price, description, stock, etc.) into one or more optimized CSV files, as well as the cover images.

## 💻 Installation and Execution Instructions

### Prerequisites

- **Python 3** (version 3.6 or higher recommended)
- **Git**

### 1. Get the Project

Navigate to your desired folder, then clone the repository:

git clone https://github.com/Mnr04/book-scraper-python.git

### 2 . Set up the virtual environment

Windows (Powershell) -- > python -m venv env .\env\Scripts\activate 

MacOS / Linux (Terminal) -->  python3 -m venv env source env/bin/activate

### 3. Install Required Packages

Once the environment is activated, install the necessary dependencies (requests, beautifulsoup4, pandas, etc.):

pip install -r requirements.txt

### 4. Run the Program

Execute the main script:

Windows -->  python main.py 

MacOS / Linux -->  python3 main.py