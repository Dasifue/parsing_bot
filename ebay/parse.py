from bs4 import BeautifulSoup as BS

import requests

def get_response(request: str):
    request_text = "+".join(request.lower().strip().split(" "))
    full_request = "https://www.ebay.com/sch/i.html?_from=R40&_trksid=p2334524.m570.l1313&_nkw="+request_text+"&_sacat=0&LH_TitleDesc=0&_odkw="+request_text+"&_osacat=0"
    request_data = requests.get(full_request)
    if request_data.status_code == 200:
        return request_data.text
    else:
        raise Exception("Error 400: Bad request")
    

def get_object_data(html):
    data = []
    soup = BS(html, 'html.parser')
    producs_list = soup.find("div", class_="srp-river-results clearfix")
    products = producs_list.find_all("div", class_="s-item__wrapper clearfix")
    for product in products:
        details = product.find("div", class_="s-item__info clearfix")
        link = details.find("a").get("href")
        name = details.find("div", class_="s-item__title").text
        price = details.find("div", class_="s-item__details clearfix").find("span", class_="s-item__price").text
        shipping = details.find("div", class_="s-item__details clearfix").find("span", class_="s-item__shipping s-item__logisticsCost").text
        data.append(
            {
            "name": name,
            "price": price,
            "shipping": shipping,
            "link": link
            }
        )
    return data



def main(request):
    try:
        html = get_response(request)
    except Exception:
        return "Data not found"
    else:
        data = get_object_data(html)
        with open(request + " ebay", mode="w", encoding="utf-8") as file:
            for object in sorted(data, key=lambda x: x["price"]):
                line = ""
                for i in object.values():
                    line += f"{i}, "
                line+="\n"
                file.write(line)
        

main("rtx 3060")