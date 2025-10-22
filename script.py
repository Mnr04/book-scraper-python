import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from function import fetch_category_urls, retrieve_book_url, save_to_csv, download_img,one_book_data


html = 'https://books.toscrape.com/'
    
urls_category = fetch_category_urls(html)
print('category finish to fetch')
#Loop through each category
for url in urls_category:
    all_books_urls= retrieve_book_url(url, html)
print('All books urls are fetch')
print('start scrapping book')
print(len(all_books_urls))

#Problem here verify all the code
for books in all_books_urls:
    data, img_src, book_title, category_name = one_book_data(books)
    download_img(img_src, category_name, book_title)
    df = save_to_csv(category_name, data)
    print(f'category {category_name } Finished with {len(df)} registred') 


