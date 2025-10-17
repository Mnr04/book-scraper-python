import requests
from bs4 import BeautifulSoup
import re

# On recupere le html de la page 
html = 'https://books.toscrape.com/catalogue/the-black-maria_991/index.html'
response = requests.get(html)

#affiche le code de reponse
#print(response.status_code)

soup = BeautifulSoup(response.text, 'html.parser')
#print(soup)

"""
Donnée à récupérer:

● product_page_url (on recupere le href du a)
    #div(class:page_inner) > ul(class: breadcrumb) > li3 > a

● product_description
    #div(id:product_description) > p
"""
# upc
data_upc = soup.find("table", class_ = 'table table-striped')
upc_element = data_upc.find_all("td")
print(f"upc code : {upc_element[0].text}")

#Title
data_title = soup.find("div", class_ = 'col-sm-6 product_main')
title_element = data_title.find("h1")
print(f"Title : {title_element.text}")

#price_including_tax (gerer le regex)
data_price_including_tax = soup.find("table", class_ = 'table table-striped')
price_including_tax = data_price_including_tax.find_all("td")
print(f"price including tax : {price_including_tax[3].text}")

#price_excluding_tax (gerer le regex)
data_price_excluding = soup.find("table", class_ = 'table table-striped')
price_excluding_tax = data_price_excluding.find_all("td")
print(f"price including tax : {price_excluding_tax[2].text}")

#Number available (gerer le regex)
data_number_available = soup.find("table", class_ = 'table table-striped')
number_available = data_number_available.find_all("td")
print(f"number_available : {number_available[5].text}")

# product_description 
data_product_description = soup.find("div", id = 'product_description')
product_description = data_product_description.find_next("p")
print(f"description : {product_description.text}")

# category(on recupere le texte du a)
data_category = soup.find('ul', class_='breadcrumb')
category = data_category.find_all("li")
print(f"category: {category[2].text}")

#Stars_rating
star_rating = soup.find('p' , class_ = "star-rating")
print(f" nombre d'etoiles {star_rating.attrs['class'][1]}")

#image_url (Rajouter Url du site devant le img)
data_img = soup.find('div', class_='item active')
img = data_img.find('img')
print(f"img src: {img.attrs['src']}")

