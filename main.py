from functions import fetch_category_urls, retrieve_book_url, save_to_csv, download_img,one_book_data
from tqdm import tqdm


def main():
    # Base URL of the website to be scraped
    html = 'https://books.toscrape.com/'

    print(f"Welcome in BookScraper! Starting scraping: {html}")

    #Fetch the list of all category URLs available on the homepage.
    urls_category = fetch_category_urls(html)

    #Loop Through Categories to Get Book URLs
    print("Fetching book URLs by category...")

    for url in tqdm(urls_category):
        all_books_urls= retrieve_book_url(url, html)

    print("Successfully fetched all book URLs by category.")

    #fMain Scraping from each url, Image Download, and Saving in CSV files
    print("Starting main process: Scraping URLs, downloading images, and saving to CSV files...")

    for books in tqdm(all_books_urls):
        data ,img_src, upc, category_name = one_book_data(books)
        download_img(img_src, category_name, upc)
        save_to_csv(category_name, data)

    print("Main process complete: Data scraped, images downloaded, and CSV files saved successfully.")
    
if __name__ == "__main__":
    main()


