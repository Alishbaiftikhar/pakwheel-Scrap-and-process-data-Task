import requests
from bs4 import BeautifulSoup

URL = "https://www.pakwheels.com/used-cars/search/-/mk_suzuki/md_alto/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
links = soup.find_all("a", attrs={'class': 'car-name ad-detail-path'})

# print(links)
link = links[0].get('href')
product_list = "https://www.pakwheels.com/" + link
print(product_list)
new_webpage = requests.get(product_list, headers=headers)
print(new_webpage)
new_soup = BeautifulSoup(new_webpage.content, "html.parser")
print(new_soup)