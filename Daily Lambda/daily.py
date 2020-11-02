from github import Github

import pandas as pd
import numpy as np

import requests
from lxml.html import fromstring

from datetime import datetime as dt
from pytz import timezone

# page targets
halls = [
    'Bursley',
    'East Quad',
    'Markley',
    'Mosher-Jordan',
    'North Quad',
    'South Quad',
    'Twigs at Oxford',
    'MDining To-Go/Kosher Kitchen',
    'MDining To-Go/Central Campus Recreation Building',
    'MDining To-Go/Michigan Union',
    'MDining To-Go/South Quad',
]

# scrape from page HTML
getTitles = lambda: tree.xpath('//span[@class="calhours-title"]/text()')

getTimes = lambda: [time.replace('\xa0', ' ') for time in tree.xpath('//span[@class="calhours-times"]/text()')]

getCourses = lambda: [div.xpath('.//div[@class="item-name"]/text()') for div in tree.xpath('//div[@class="courses"]')]

tz = timezone("America/Detroit")
ptime = lambda string, form: dt.strptime(string, form).time()
now = lambda: dt.now(tz).strftime('%-d %b %Y %-I:%M %p')

tree = 0
def execute(hall):
    link = 'https://dining.umich.edu/menus-locations/dining-halls/' + hall.replace(' ', '-')
    r = requests.get(link)
    global tree
    tree = fromstring(r.content)

    labels = [text.strip() for text in set(tree.xpath('//a[@href="#"]/text()'))]
    top = [(title, time) for title, time in zip(getTitles(), getTimes()) if title in labels]
    return [(hall, title, time, course) for (title, time), course in zip(top, getCourses())]

headers = 'Hall Meal Time Foods'.split()
table = [x for hall in halls for x in execute(hall)]
df = pd.DataFrame(dict(zip(headers, np.array(table, dtype=object).T)))

# update GitHub
API_KEY = "YOUR KEY HERE"
g = Github(API_KEY)

repo = g.get_repo("GeorgeFane/MDining-Scraper")
contents = repo.get_contents("scraped.txt")
repo.update_file(contents.path, 'Updated ' + now(), df.to_csv(), contents.sha, branch="master")

print('done')
