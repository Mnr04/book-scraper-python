import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from halo import Halo


urls_category = []
all_books_data = []
all_books_urls = []

#A function to fetch category URLs.
def fetch_category_urls(html) -> list:
    """
    Fetches the full URLs for all book categories on the page.

    Args:
        html (str): The base URL of the website containing the category list.

    Returns:
        list: A list of strings, where each string is the absolute URL
              of a book category page.
    """
    print("Starting to fetch the full URLs for all book categories on the page.")
    spinner = Halo(text='Loading', spinner='dots')
    spinner.start()
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get the links for each category:
    for li in soup.find('div', class_ = 'side_categories').find_all('li')[1:]:
        full_link = html  + li.find('a').attrs['href']
        urls_category.append(full_link)
    spinner.stop()
    print("All URLs fetched successfully.")
    return urls_category

#A function to retrieve book URLs by category.
def retrieve_book_url(url, html):
    """Retrieves all book URLs from a category, handling pagination.

    Scrapes a category's first page and follows all 'next' page links
    to gather the absolute URLs for every book in that category.

    Args:
        url (str): The URL of the category's first page.
        html (str): The website's base URL for constructing full book URLs.

    Returns:
        list: A list of strings, containing the full, absolute URLs
              for all books found in the category.
    """
    # La fonction on lui donne une categorie elle retourne tout les urls des livres de cette categorie
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Retrieve book URLs from the first page
    section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for li in section:
        link_data = li.find('a')
        # Constructs the full URL by combining the base HTML and cleaning the relative path
        full_book_url = html +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
        all_books_urls.append(full_book_url)
        # If a second page is detected, loop to follow the 'next' link 
    while soup.find('li', class_ = 'next'):
        # Get the relative URL for the next page
        next_url = soup.find('li', class_ = 'next').find('a').attrs['href']
        # Split the category URL
        category_base_url = (re.split('/index.html', url))[0] 
        # Construct the full URL for the next page
        full_next_page_url = category_base_url + '/' + next_url
        # Send a request to the next page and update the soup object
        response = requests.get(full_next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

        # Retrieve book URLs from the subsequent pages
        section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for li in section:
            link_data = li.find('a')
            # Constructs the full URL for the book
            full_book_url = html +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
            all_books_urls.append(full_book_url)
    return all_books_urls

#A function to extract all book data.
def one_book_data(html):
    """
        Extracts book data from the provided HTML page.

        Args:
            html (str): The HTML content of the book page to be scraped.

        Returns:
            dict : A dictionary containing the extracted data for the book.
    """
    data = {}
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Product Page
    data['Product_Page'] = html


    # U.P.C.
    try:
        data_upc = soup.find("table", class_ = 'table table-striped').find_all("td")
        data['universal_ product_code (upc)'] = data_upc[0].text
        upc = data_upc[0].text
    except:
        data['universal_ product_code (upc)'] = 'Not Available'

    # Title
    try:
        data_title = soup.find("div", class_ = 'col-sm-6 product_main').find("h1")
        clean_title_text = re.sub(r"/", " ", data_title.text)
        data['Title'] = clean_title_text
    except:
        data['Title'] = 'Not Available'

    # Price including tax
    try:
        data_price_including_tax = soup.find("table", class_ = 'table table-striped').find_all("td")
        price_including_tax = re.split(r"£", data_price_including_tax[3].text)
        data['price_including_tax'] = price_including_tax[1]
    except:
        data['price_including_tax'] = 'Not Available'

    # Price excluding tax
    try:
        data_price_excluding = soup.find("table", class_ = 'table table-striped').find_all("td")
        price_excluding = re.split(r"£", data_price_excluding[2].text)
        data['price_excluding_tax'] = price_excluding[1]
    except:
        data['price_excluding_tax'] = 'Not Available'

    # Number available
    try:
        data_number_available = soup.find("table", class_ = 'table table-striped').find_all("td")
        number_available = re.findall(r"\d+", data_number_available[5].text)
        data['number_available'] = number_available[0]
    except:
        data['number_available'] = 'Not Available'

    # Product description 
    try : 
        data_product_description = soup.find("div", id = 'product_description').find_next("p")
        data['product_description'] = data_product_description.text
    except :
        data['product_description'] = 'Not Available' 

     #Category Name
    try:
        data_category = soup.find('ul', class_ = 'breadcrumb')
        li_href = data_category.find_all('li')
        category_name = li_href[2].text
        #clean \n
        category_name = re.sub(r"\n", "", category_name)
        data['category'] = category_name
    except : 
        print("no category name find")

    # Stars_rating
    try:
        star_rating = soup.find('p' , class_ = "star-rating")
        stars_number = star_rating.attrs['class'][1]
        
        if stars_number == "One":
            stars_number = 1
        elif stars_number == "Two":
            stars_number = 2
        elif stars_number == "Three":
            stars_number = 3
        elif stars_number == "Four":
            stars_number = 4
        elif stars_number == "Five":
            stars_number = 5
        else:
            stars_number = 0 
            
        data['review_rating'] = stars_number
    except:
        data['review_rating'] = 0 

    # image_url
    try:
        data_img = soup.find('div', class_='item active').find('img')
        data['image_url'] = "https://books.toscrape.com" + "/" + re.sub(r"\.\./\.\./", "",data_img.attrs['src'])
        img_src = data['image_url']
    except:
        data['image_url'] = 'Not Available'
    return data, img_src, upc, category_name

#A function to download and save images.
def download_img(img_src, category_name, upc):
    """Downloads an image and saves it into a specific category folder.

    Args:
        img_src (str): The URL of the image to download.
        category_name (str): The name of the subfolder to save the image in.
        book_title (str): The base name for the saved image file.
    """
    response = requests.get(img_src)
    category_name = category_name 
    file_name = upc + '.jpg'
    #create directory img files
    directory_file = "img_downloads"
    os.makedirs(directory_file, exist_ok=True)
    folder_path = os.path.join( directory_file, category_name )
      # The 'exist_ok=True' parameter prevents an error if the directory is already present 
    os.makedirs(folder_path, exist_ok=True)
    #Construct the full file path
    file_path = os.path.join(folder_path, file_name)
    # Open the file path in write binary mode and save the content.
    with open(file_path, 'wb') as file:
        file.write(response.content)
      
#A function to save data to a CSV file.
def save_to_csv(category_name, data):
    """Appends a dictionary of data as a new row to a CSV.

    Args:
        category_name (str): The category used to name the target CSV file.
        data (dict): The data row to append to the CSV.
    """
    CSV_HEADERS = [
    'Product_Page', 
    'universal_ product_code (upc)', 
    'Title', 
    'price_including_tax', 
    'price_excluding_tax', 
    'number_available', 
    'product_description', 
    'category', 
    'review_rating', 
    'image_url' 
    ]
    # Create path
    directory_file = 'Books_data_csv'
    file_path = f'{directory_file}/{category_name}_Books_data.csv'
    # Create folder 
    os.makedirs(directory_file, exist_ok=True)
    #write header for new files
    write_header = not os.path.exists(file_path)

    df = pd.DataFrame([data])
    df.to_csv(file_path, mode='a', header=write_header, index=False, columns=CSV_HEADERS)