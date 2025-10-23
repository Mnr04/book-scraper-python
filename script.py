from function import fetch_category_urls, retrieve_book_url, save_to_csv, download_img,one_book_data

# Base URL of the website to be scraped
html = 'https://books.toscrape.com/'

#Fetch the list of all category URLs available on the homepage.
urls_category = fetch_category_urls(html)

#Loop Through Categories to Get Book URLs
for url in urls_category[:4]:
    all_books_urls= retrieve_book_url(url, html)

#fMain Scraping from each url, Image Download, and Saving in CSV files
for books in all_books_urls[55:]:
    data ,img_src, book_title, category_name = one_book_data(books)
    download_img(img_src, category_name, book_title)
    save_to_csv(category_name, data)
    


