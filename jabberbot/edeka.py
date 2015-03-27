#!/usr/bin/env python
import requests
import re
from bs4 import BeautifulSoup
from datetime import datetime, date

_DATE_REGEX = r"\d\d[.]\d\d[.]\d\d"
_DATE_FORMAT = '%d.%m.%y'
_DATE_WHOLEDAY_FORMAT = '%A, ' + _DATE_FORMAT
_EDEKA_URL = "http://simmel.de/wochenmenue/muenchen"

class EdekaMeal:
    def __init__(self, mealHtml):
        self.meal = mealHtml.find('div', {'class' : 'value'}).text
        self.price = mealHtml.find('div', {'class' : 'price'}).text

    def __str__(self):
        return str(self.meal) + ': ' + str(self.price)

class EdekaDay:
    def __init__(self, dayHtml):
        print(dayHtml)
        self.date = datetime.strptime(re.findall(_DATE_REGEX, dayHtml.find('h5').text)[0], _DATE_FORMAT)
        self.meals = self._createMeals(dayHtml.find_all('div', {'class' : 'item'}))

    def _createMeals(self, mealsArray):
        mealList = []
        for meal in mealsArray:
            mealList += [EdekaMeal(meal)]
        return mealList

    def __str__(self):
        resultString = self.date.strftime(_DATE_WHOLEDAY_FORMAT) + "\n"
        for meal in self.meals:
            resultString += str(meal) + "\n"
        return resultString

class EdekaWeekMenu:
    def __init__(self, weekHtml):
        weekString = weekHtml.find('h4').text
        weekDates = re.findall(_DATE_REGEX, weekString)
        self.startDay = datetime.strptime(weekDates[0], _DATE_FORMAT)
        self.endDay = datetime.strptime(weekDates[1], _DATE_FORMAT)
        self.days = self._createDays(weekHtml.find_all('div', {'class' : 'market-menu'}))

    def isInWeek(self, date):
        return self.startDay.date() <= date <= self.endDay.date()

    def getDayMenu(self, date):
        for day in self.days:
            if day.date.date() == date:
                return day
        return 'Edeka ist defekt. Techniker ist informiert.'

    def _createDays(self, daysArray):
        dayList = []
        for day in daysArray:
            dayList += [EdekaDay(day)]
        return dayList

    def __str__(self):
        resultString = 'Week from ' + self.startDay.strftime(_DATE_FORMAT) + ' to ' + self.endDay.strftime(_DATE_FORMAT) + "\n"
        for day in self.days:
            resultString += str(day)
        return resultString

def Edeka(message, *args):
    """Return the weekly Edeka lunch menu

    You can get the meal for the whole week: !edeka week
    Or even the next week: !edeka next week"""

    # modes:
    # 0 -> meal of the day
    # 1 -> meal of this week
    # 2 -> meal of next week
    mode = 0
    if args:
        if args[0] == 'week':
            mode = 1
        elif args[0] == 'next' and args[1] == 'week':
            mode = 2

    request  = requests.get(_EDEKA_URL)
    data = request.text
    soup = BeautifulSoup(data)

    weeks = soup.find_all("div", { "class" : "element" })
    edekaWeekMenus = []
    for week in weeks:
        edekaWeekMenus += [EdekaWeekMenu(week)]

    if mode == 0:
        today = date.today()
        for week in edekaWeekMenus:
            if week.isInWeek(today):
                return str(week.getDayMenu(today))
    elif mode == 1:
        return str(edekaWeekMenus[0])
    elif mode == 2:
        try:
            return str(edekaWeekMenus[1])
        except IndexError:
            return 'Next week\'s menu is not available yet!'

    return 'Edeka ist defekt. Techniker ist informiert.'
