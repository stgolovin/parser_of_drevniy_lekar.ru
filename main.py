import requests
from bs4 import BeautifulSoup
import csv
import time

headers = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.3 Safari/605.1.15"
}

url = 'https://drevniy-lekar.ru/katalog/bal_zamy_na_travah'
# response = requests.get(url, headers=headers)
# src = response.text

# with open('index.html', 'w') as file:
#     file.write(src)

with open('index.html') as file:
    data = file.read()

soup = BeautifulSoup(data, 'html.parser')

# collect links to each item
links = soup.find_all(class_='ksm-catalog-item')
# print(links[0].find('a').get('href'))


links_list = list()
index = 0
for elem in range(len(links)):
    links_list.append(links[index].find('a').get('href'))
    index += 1
new_links_list = list()

for chunk in links_list:
    new_links_list.append(f'https://drevniy-lekar.ru{chunk}')

with open ('data_collection', 'w', encoding='utf=8') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerow(
        (
        'Title',
        'Description',
        )
    )

for elem in new_links_list:
    time.sleep(15)
    response = requests.get(elem, headers=headers)
    src = response.text
    soup_of_items = BeautifulSoup(src, 'html.parser')
    title = soup_of_items.find(class_='ksm-product-title')
    description = soup_of_items.find(class_='ksm-product-tabs-content ksm-product-tabs-content-description active')
    photo_url = soup_of_items.find(class_='ksm-product-gallery-bigs').find('img').get('src')
    with open('images/%s' % f'{title.text}.jpg', 'wb') as file:
        img = requests.get(photo_url)
        file.write(img.content)

    with open ('data_collection', 'a', encoding='utf=8') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            (
            title.text,
            description.text,
            )
        )
