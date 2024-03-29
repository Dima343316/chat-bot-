import cards as cards
import requests
from bs4 import BeautifulSoup
import csv

CSV = 'cards.csv'
HOST = 'https://minfin.com.ua/'
URL = 'https://minfin.com.ua/cards/debit/'
HEADERS = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/99.0.4844.84 Safari/537.36'
}

def get_html(url, params=''):
    r = requests.get(URL, headers=HEADERS, params=params)
    return r

def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='be80pr-1 gdrIQA')
    cards = []

    for item in items:
        cards.append(
            {
                'title': item.find('div', class_='be80pr-15 kwXsZB').find(class_ = 'cpshbz-0 eRamNS').get_text(),
                'link_product': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').find('a').get('href'),
                'brand': item.find('div', class_='be80pr-16 be80pr-17 kpDSWu cxzlon').find('a').get_text(),
                'image': HOST + item.find('div', class_='be80pr-9 fJFiLL').find('img').get('src')
            }
        )
    return cards




def save_doc(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Название карт', 'Ссылка на продукт', 'Банк', 'Изображение карты'])
        for item in items:
            writer.writerow( [item['title'], item['link_product'], item['brand'], item['image']])



def parser():
    html = get_html(URL)
    if html.status_code == 200:
        cards = []
    cards.extend(get_content(html.text))
    save_doc(cards, CSV)

parser()