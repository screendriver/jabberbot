#!/usr/bin/env python
import requests
from bs4 import BeautifulSoup

def Edeka(message, *args):
    """ Return the weekly Edeka lunch menu"""

    r  = requests.get("http://simmel.de/wochenmenue/muenchen")
    data = r.text
    soup = BeautifulSoup(data)

    weeks = soup.find_all("div", { "class" : "element" })
    resultString = ''
    for week in weeks:
        resultString += week.find('h4').text + "\n\\"
        for day in week.find_all('div', {'class' : 'market-menu'}):
            resultString += day.find('h5').text + "\n"
            for meal in day.find_all('div', {'class' : 'item'}):
                resultString += meal.find('div', {'class' : 'value'}).text + ': ' + meal.find('div', {'class' : 'price'}).text + "\n"

    return str(resultString.encode('utf-8'))
