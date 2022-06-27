import requests
from bs4 import BeautifulSoup
import json

URL = "https://rozetka.com.ua/ua/notebooks/c80004/producer=razer;seller=other,rozetka/"
HEADERS = {
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.0.0 Safari/537.36",
    "accept": "*/*"
}


def get_html(url, params=None):
    r = requests.get(url=url, auth=('user', 'pass'), headers=HEADERS, params=params)
    return r


def get_page(html):
    soup = BeautifulSoup(html.text, "lxml")
    pagination = soup.find_all("li", class_="pagination__item")
    if pagination:
        return int(pagination[-1].get_text())
    else:
        return 1

def get_content(html):
    soup = BeautifulSoup(html.text, "lxml")
    items = soup.find_all("div", class_="goods-tile__inner")


    laptops = []
    for item in items:
        price_old = item.find("div", class_="goods-tile__price--old price--gray ng-star-inserted").text.replace(" ", "").strip()

        laptop = {
            "name_model": item.find("span", class_="goods-tile__title").text.strip().replace("\"", "").replace("������� ", ""),
            "model_url": item.find("a", class_="goods-tile__heading ng-star-inserted").get("href"),
            "model_price_now": item.find("p", class_="ng-star-inserted").text.replace(" ", " ").strip(),
        }

        if price_old:
            laptop["model_price_old"] = price_old
        else:
            laptop["model_price_old"] = "старої ціни нема"

        laptops.append(laptop)

    return laptops



def parser():
    html = get_html(URL)

    if html.status_code == 200:
        pages = get_page(html)
        laptops = []
        for page in range(1, pages + 1):
            print(f"Іде процес, спарсино {page} з {pages}...")
            html = get_html(URL, params={"page": page})
            laptops.append(get_content(html))

        with open("parse_rozetka.json", "w", encoding="utf-8") as f:
            json.dump(laptops, f, indent=4, ensure_ascii=False)
    else:
        print("no")


if __name__ == "__main__":
    parser()


