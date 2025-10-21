import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
all_books_data = []


def one_book_data(html):
    data = {}
    response = requests.get(html)
    soup = BeautifulSoup(response.text, 'html.parser')
    #Product Page
    data['Product_Page'] = html
    #Upc
    data_upc = soup.find("table", class_ = 'table table-striped').find_all("td")
    data['U.P.C.'] = data_upc[0].text
    #Title
    data_title = soup.find("div", class_ = 'col-sm-6 product_main').find("h1")
    data['Title'] = data_title.text
    #price_including_tax 
    data_price_including_tax = soup.find("table", class_ = 'table table-striped').find_all("td")
    price_including_tax = re.split(r"£", data_price_including_tax[3].text)
    data['Price including tax'] = price_including_tax[1]
    #price_excluding_tax 
    data_price_excluding = soup.find("table", class_ = 'table table-striped').find_all("td")
    price_excluding = re.split(r"£", data_price_excluding[2].text)
    data['Price excluding tax'] = price_excluding[1]
    #Number available 
    data_number_available = soup.find("table", class_ = 'table table-striped').find_all("td")
    number_available = re.findall(r"\d+", data_number_available[5].text)
    data['Number available'] = number_available[0]
    # product_description 
    data_product_description = soup.find("div", id = 'product_description').find_next("p")
    data['Product description'] = data_product_description.text
    # category(
    data_category = soup.find('ul', class_='breadcrumb').find_all("li")
    category = re.sub("\n", "", data_category[2].text)
    data['Category'] = category
    #Stars_rating
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
    data['star number'] = stars_number
    #image_url 
    data_img = soup.find('div', class_='item active').find('img')
    data['img src'] = "https://books.toscrape.com" + "/" + re.sub(r"\.\./\.\./", "",data_img.attrs['src'])

    all_books_data.append(data)
    return all_books_data

def save_to_csv(all_books_data):
    df = pd.DataFrame(all_books_data)
    df.to_csv('Books_data.csv')
    return print("data save in Books_data.csv")

def url_scraping(category_url):
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for li in section:
        link_data = li.find('a')
        full_book_url = base_url +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
        
        return full_book_url

    
with requests.Session() as session : 
 
    base_url  = 'https://books.toscrape.com'
    category_url = 'https://books.toscrape.com/catalogue/category/books/travel_2/index.html'
        
    response = requests.get(category_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for li in section:
        link_data = li.find('a')
        full_book_url = base_url +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
    one_book_data(full_book_url)

   
    while soup.find('li', class_ = 'next'):

        next_url = soup.find('li', class_ = 'next').find('a').attrs['href']
        category_base_url = (re.split('/index.html', category_url))[0] 
        full_next_page_url = category_base_url + '/' + next_url
        response = requests.get(full_next_page_url)
        soup = BeautifulSoup(response.text, 'html.parser')

    section = soup.find('section').find_all('li', class_ = 'col-xs-6 col-sm-4 col-md-3 col-lg-3')
    for li in section:
        link_data = li.find('a')
        full_book_url = base_url +  '/catalogue' + re.sub(r"\.\./\.\./\.\.", "", link_data.attrs['href']) 
        one_book_data(full_book_url)

    else: print('stop')

    save_to_csv(all_books_data)


