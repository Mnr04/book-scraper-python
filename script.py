import requests
from bs4 import BeautifulSoup
import re
import pandas as pd

url_category = []

def one_book_data(html):
    """
        Extracts book data from the provided HTML page.

        Args:
            html (_type_): The HTML content of the book page to be scraped.

        Returns:
            _type_: A dictionary containing the extracted data for the book.
    """
    data = {}
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')
    # Product Page
    data['Product_Page'] = html

    # U.P.C.
    try:
        data_upc = soup.find("table", class_ = 'table table-striped').find_all("td")
        data['U.P.C.'] = data_upc[0].text
    except:
        data['U.P.C.'] = 'Not Available'

    # Title
    try:
        data_title = soup.find("div", class_ = 'col-sm-6 product_main').find("h1")
        data['Title'] = data_title.text
    except:
        data['Title'] = 'Not Available'

    # Price including tax
    try:
        data_price_including_tax = soup.find("table", class_ = 'table table-striped').find_all("td")
        price_including_tax = re.split(r"£", data_price_including_tax[3].text)
        data['Price including tax'] = price_including_tax[1]
    except:
        data['Price including tax'] = 'Not Available'

    # Price excluding tax
    try:
        data_price_excluding = soup.find("table", class_ = 'table table-striped').find_all("td")
        price_excluding = re.split(r"£", data_price_excluding[2].text)
        data['Price excluding tax'] = price_excluding[1]
    except:
        data['Price excluding tax'] = 'Not Available'

    # Number available
    try:
        data_number_available = soup.find("table", class_ = 'table table-striped').find_all("td")
        number_available = re.findall(r"\d+", data_number_available[5].text)
        data['Number available'] = number_available[0]
    except:
        data['Number available'] = 'Not Available'

    # Product description (déjà avec try/except, conservé tel quel)
    try : 
        data_product_description = soup.find("div", id = 'product_description').find_next("p")
        data['Product description'] = data_product_description.text
    except :
        data['Product description'] = 'Not Available' 

    # Category
    try:
        data_category = soup.find('ul', class_='breadcrumb').find_all("li")
        category = re.sub("\n", "", data_category[2].text)
        data['Category'] = category
    except:
        data['Category'] = 'Not Available'

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
            
        data['star number'] = stars_number
    except:
        data['star number'] = 0 

    # image_url
    try:
        data_img = soup.find('div', class_='item active').find('img')
        data['img src'] = "https://books.toscrape.com" + "/" + re.sub(r"\.\./\.\./", "",data_img.attrs['src'])
    except:
        data['img src'] = 'Not Available'
    all_books_data.append(data)
    return all_books_data

def save_to_csv(category_name, all_books_data):
    df = pd.DataFrame(all_books_data)
    df.to_csv(f'Books_data_{category_name}.csv')
    return df

with requests.Session() as session : 

    html = 'https://books.toscrape.com/'
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')

    #Get the links for each category:
    category_element = soup.find('div', class_ = 'side_categories').find_all('li')[1:]
    for li in category_element:
        full_link = html  + li.find('a').attrs['href']
        url_category.append(full_link)
        
    #Loop through each category
    for url in url_category:
        all_urls = []
        all_books_data = []
        #print(f'on commence la category {url}')
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')

        #Get the category book
        category_name = soup.find('div', class_='page-header action').find('h1').text
        print(f'start scraping {category_name} category')
        # Retrieve book URLs from the first page
        section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
        for li in section:
            link_data = li.find('a')
            # Constructs the full URL by combining the base HTML and cleaning the relative path
            full_book_url = html +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
            all_urls.append(full_book_url)

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
                all_urls.append(full_book_url)
        # For each book URL, start the scraping and save the data to CSV
        for element in all_urls:
            one_book_data(element)
            df = save_to_csv(category_name, all_books_data)
        print(f'category {category_name } Finished with {len(df)} registred')

