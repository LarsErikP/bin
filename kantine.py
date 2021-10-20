#!/usr/bin/python3

import datetime
import re
import sys
import requests
from bs4 import BeautifulSoup

menu_dict = {}
today = datetime.datetime.today().weekday()
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
    remove = 'Plukk og mix'

    for element in menu:
        day = element.find("h4").text.strip().lower()
        dishes = element.find_all("li", class_="dishes__dishes__dish")
        for dish in dishes:
            if not re.findall(remove, dish.text):
                menu_dict[day] = dish.contents[0].strip().replace(', fisk og vegetar', '')

## Program starts here ##
#########################
if len(sys.argv) < 2:
    fetch_menu()
    for day, food in menu_dict.items():
        print("{}: {}".format(day.capitalize(), food))
elif len(sys.argv) == 2:
    search = sys.argv[1].lower()
    if re.search('dag', search):
        fetch_menu()
        print(menu_dict[search])
    else:
        fetch_menu()
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
    print("Feil antall argumenter, din lauk!")
