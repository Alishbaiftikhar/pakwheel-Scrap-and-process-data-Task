import requests
from bs4 import BeautifulSoup
import pika;

URL = "https://www.pakwheels.com/used-cars/search/-/mk_suzuki/md_alto/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36"
}
page = requests.get(URL, headers=headers)

soup = BeautifulSoup(page.content, "html.parser")
links_list = []
title=[]
place=[]
count=0
links = soup.find_all("a", attrs={'class': 'car-name ad-detail-path'})

# print(links)
for link in links:
            links_list.append(link.get('href'))
for link in links_list:
    count=count+1
    product_list = "https://www.pakwheels.com/" + link
    # print(product_list)
    new_webpage = requests.get(product_list, headers=headers)
    # print(new_webpage)
    new_soup = BeautifulSoup(new_webpage.content, "html.parser")
    # print(new_soup)
    title = new_soup.find("h1").text.strip()
    # print(title)
    place=new_soup.find("p",attrs={'class':'detail-sub-heading'}).a.get_text()
    # print(place)
    # seller=new_soup.find("h5",attrs={'class':'nomargin'}).text.strip()
    # print(seller)
    engine_element = new_soup.find('li', string='Engine Capacity')
    if engine_element:
     engine = engine_element.find_next_sibling('li').get_text()
    #  print(engine)
    else:
     engine=''
    registered_element=new_soup.find('li', string='Registered In')
    if registered_element:
        registered=registered_element.find_next_sibling('li').get_text()
        print(registered)
    else:
     registered=''

    ul_element = new_soup.find('ul', class_='light-gallery')
    # print(ul_element)
    li_elements = ul_element.find_all('li')
    # print(li_elements)
    image_links = []
    price = new_soup.find('strong', class_='generic-green').text.strip()
    # print(price)
    for li in li_elements:
        data_src = li.get('data-src')
        if data_src:
            image_links.append(data_src)
    
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='data_queue')
    data = {
    'title': title,
    'place':place,
    'image_links': image_links,
    'price':price,
    'engine':engine,
    'registered':registered,
    'count':count
    }
    # Send the data as a message
    channel.basic_publish(exchange='', routing_key='data_queue', body=str(data))

    # Close the connection
    connection.close()

    # Print the list of image links
    # for link in image_links:
    #     print(link)




