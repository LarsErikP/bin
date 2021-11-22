#!/usr/bin/python3

import datetime
import re
import sys
import requests
import locale
from bs4 import BeautifulSoup

locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8')

menu_dict = {}
today = datetime.datetime.today().weekday()
literal_today = datetime.datetime.now().strftime("%A")
week_translation = {
        'mandag': 0,
        'tirsdag': 1,
        'onsdag': 2,
        'torsdag': 3,
        'fredag': 4
        }

def fetch_menu():
    URL = 'https://www.sit.no/gjovik/mat'
    user_agent =  {'User-Agent': 'Mozilla/5.0(X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}
    page = requests.get(URL, headers=user_agent)
    soup = BeautifulSoup(page.content, "html.parser")
    menu = soup.find_all("li", class_="dishes__day")
    remove = 'Plukk og mix|\|'

    for element in menu:
        day = element.find("h4").text.strip().lower()
        dishes = element.find_all("li", class_="dishes__dishes__dish")
        for dish in dishes:
            if not re.findall(remove, dish.text):
                menu_dict[day] = re.sub(r',\s*fisk og vegetar', '', dish.contents[0].strip())

## Program starts here ##
#########################
if len(sys.argv) > 2:
    print("Feil antall argumenter, din lauk!")
elif len(sys.argv) == 2:
    fetch_menu()
    search = sys.argv[1].lower()
    if search in week_translation.keys():
        print(menu_dict[search])
    elif search == 'meny':
        for day, food in menu_dict.items():
            print("{}: {}".format(day.capitalize(), food))
    elif search == 'fisk':
        print("JADA!!!! Det er fisk i dag også!!!")
    else:
        found=False
        for day, food in menu_dict.items():
            if re.search(search, food, flags=re.I):
                _day=day.lower()
                _food=food.lower()
                found=True
                if today <= week_translation[_day]:
                    print("Hurra, de serverer {} på {}!!!".format(_food, _day))
                else:
                    print("Pokker, de hadde {} denne uka, men det var på {}".format(_food, _day))
        if not found:
            print("Pokker, ikkeno {} denne uka :-(".format(search.lower()))
else:
    fetch_menu()
    print("I dag serveres: {}".format(menu_dict[literal_today]))
