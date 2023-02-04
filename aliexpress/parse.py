from bs4 import BeautifulSoup as BS

import requests

from config import URL, CPUS


def get_response(request: str):
    request_text = "+".join(request.lower().strip().split(" "))
    full_request = "https://aliexpress.ru/wholesale?SearchText="+request_text
    request_data = requests.get(full_request)
    if request_data.status_code == 200:
        return request_data.text
    else:
        raise Exception("Error 400: Bad request")
    

def is_matching(request, name):
    request = request.lower().replace(" ", "-")
    name = name.lower().replace(" ", "-")
    if request in name:
        return True
    return False


def get_links(request, html):
    links = []
    soup = BS(html, 'html.parser')
    producs_list = soup.find("div", class_="product-snippet_ProductSnippet__grid__lido9p")
    products = producs_list.find_all("div", class_="product-snippet_ProductSnippet__container__lido9p product-snippet_ProductSnippet__vertical__lido9p product-snippet_ProductSnippet__imageSizeM__lido9p product-snippet_ProductSnippet__hideOptions__lido9p product-snippet_ProductSnippet__hideDiscount__lido9p product-snippet_ProductSnippet__hideCashback__lido9p product-snippet_ProductSnippet__hideSubsidy__lido9p product-snippet_ProductSnippet__hideFreeDelivery__lido9p product-snippet_ProductSnippet__hideActions__lido9p product-snippet_ProductSnippet__hideSponsored__lido9p")
    for product in products:
        detail = "product-snippet_ProductSnippet__{}__lido9p"
        description = "product-snippet_ProductSnippet__description__lido9p"
        link = URL+product.find("div", class_=description).find("a").get("href")
        name = product.find("div", class_=description).find("div", class_=detail.format("name")).text
        if is_matching(request=request, name=name):
            links.append(link)
    return links


def get_object_data(url):
    html = requests.get(url)
    soup = BS(html.text, "html.parser")
    name = soup.find("h1").text
    try:
        price = soup.find("div", class_="snow-price_SnowPrice__secondPrice__18x8np").text.replace("\xa0", " ")
        price_with_discount = soup.find("div", class_="snow-price_SnowPrice__mainS__18x8np").text.replace("\xa0", " ")
    except AttributeError:
        price = soup.find("div", class_="snow-price_SnowPrice__mainS__18x8np").text.replace("\xa0", " ")
        price_with_discount = soup.find("div", class_="snow-price_SnowPrice__mainS__18x8np").text.replace("\xa0", " ")
    finally:
        data = {
            "name": name,
            "price": price,
            "price with discount": price_with_discount
            }
    return data


def main(request):
    data = {}
    try:
        html = get_response(request=request)
        links = get_links(request=request, html=html)
    except Exception:
        return None
    else:
        for item in links:
            data.update({item:get_object_data(item)})
        return data


print(main("rtx 3060"))