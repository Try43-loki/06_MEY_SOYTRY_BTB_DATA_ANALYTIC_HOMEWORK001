from bs4 import BeautifulSoup
import requests

URL = 'https://www.womansday.com/relationships/dating-marriage/a41055149/best-pickup-lines/'

response = requests.get(URL)
soup = BeautifulSoup(response.text,'html.parser')

uls_data = soup.select('ul[class="css-1wk73g0 emevuu60"]')
pickupList = {}
items = []

for ul in uls_data:
    if ul.text == "":
        continue
    items.append(ul)
titles = soup.select('h2[title]')

for ul in range(len(items)):
    ul_data = items[ul].select('li')
    data_text = []
    for list in ul_data:
        clean_text = list.text.split("RELATED:")[0].strip()
        data_text.append(clean_text)
    pickupList.update({f"{titles[ul].text}": data_text})
    data_text = []

with open('pickup_line.json','w', encoding='utf-8') as file:
    file.write(str(pickupList))
