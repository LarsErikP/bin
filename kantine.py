#!/usr/bin/python3

import datetime
import re
import sys
import requests
import locale
from bs4 import BeautifulSoup
import json

locale.setlocale(locale.LC_TIME, 'nb_NO.UTF-8')

menu_dict = {}
today = datetime.datetime.today().weekday()
literal_today = datetime.datetime.now().strftime("%A")
week_number = int(datetime.datetime.today().strftime("%V"))
year = datetime.datetime.today().year
weekdays = ["monday", "tuesday", "wednesday", "thursday", "friday"]
weekday_translation = {
        'monday': 'mandag',
        'tuesday': 'tirsdag',
        'wednesday': 'onsdag',
        'thursday': 'torsdag',
        'friday': 'fredag'
        }
week_translation = {
        'mandag': 0,
        'tirsdag': 1,
        'onsdag': 2,
        'torsdag': 3,
        'fredag': 4
        }

def get_current_week_menu(data, week, year):
    return next((item for item in data if item.get("week") == week and item.get("year") == year), None)

def fetch_menu():
    URL = 'https://www.sit.no/mat-og-drikke/vare-spisesteder/sit-kafe-gjovik'
    user_agent =  {'User-Agent': 'Mozilla/5.0(X11; Ubuntu; Linux x86_64; rv:93.0) Gecko/20100101 Firefox/93.0'}
    page = requests.get(URL, headers=user_agent)
    soup = BeautifulSoup(page.content, "html.parser")
    data = json.loads(soup.find_all("script", id="__NEXT_DATA__")[0].text)
    allMenus = data['props']['pageProps']['data']['lookup']['weeklyMenus']
    week_menu = get_current_week_menu(allMenus, week_number, year)

    for day in weekdays:
        if day in week_menu:
            dish = week_menu[day][0]['dish']
            norwegian_day = weekday_translation[day]
            menu_dict[norwegian_day] = re.sub(r'[\.,]\s*fisk (og|eller) vege?tar', '', dish, flags=re.I)

def get_weekday_menu(weekday):
    try:
        return menu_dict[weekday]
    except KeyError:
        return "Ingen spesifikk rett på menyen i dag, så da blir det overraskelse!"

## Program starts here ##
#########################
if len(sys.argv) > 2:
    print("Feil antall argumenter, din lauk!")
elif len(sys.argv) == 2:
    fetch_menu()
    search = sys.argv[1].lower()
    if search in week_translation.keys():
        print(get_weekday_menu(search))
    elif search == 'meny':
        print("Meny for uke {}, {}".format(week_number, year))
        if (len(menu_dict)) == 0:
            print("Ukens meny har INGEN spesifikke retter! Lottouke!")
        elif (len(menu_dict)) != 5:
            print("Noen av dagene hadde litt mangelfull info, men her er det vi fant:")
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
    print("I dag serveres: {}".format(get_weekday_menu(literal_today)))
