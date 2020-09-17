import requests
from bs4 import BeautifulSoup

from datetime import datetime
from pytz import timezone

from dash import Dash
import dash_html_components as html

from dash_table import DataTable

# for a dining hall's MDining link,
# this gets all meals and hours that day
def scrape(link):
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html.parser')

    table = soup.find('div', attrs={'id': 'content'})
    titles = table.findAll('span', attrs={'class': 'calhours-title'})
    times = table.findAll('span', attrs={'class': 'calhours-times'})

    return {
        title.string: time.string.replace('\xa0', ' ')
        for title, time in zip(titles, times)
    }

# dining hall links only differ after the rightmost /
# below is the part that all links share
url = 'https://dining.umich.edu/menus-locations/dining-halls/'

halls = [
    'Bursley',
    'East Quad',
    'Markley',
    'Mosher-Jordan',
    'North Quad',
    'South Quad',
    'Twigs at Oxford'
]

# constructs links for all dining halls
links = [url+hall.replace(' ', '-') for hall in halls]

# gets meals and hours for all dining halls
rows = [scrape(link) for link in links]

# adds hall name to each hall's dictionary
for row, hall in zip(rows, halls):
    row['Hall'] = hall

headers = [
    'Hall',
    'Breakfast',
    'Brunch',
    'Lunch',
    'Dinner',
    'Late Night'
]

#stores current time in EST
tz = timezone("America/Detroit")
stamp = datetime.now(tz).strftime("%m/%d/%Y, %H:%M:%S")

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('MDining Hours'),
    html.H3('Last updated: ' + stamp),

    DataTable(
        id='table',
        columns=[
            dict(
                id=x,
                name=x,
            )
            for x in headers
        ],
        data=rows,

        sort_action="native",
        sort_mode="multi",
        page_action="native",

        style_as_list_view=True,
    ),
])

if __name__ == '__main__':
    app.run_server(port='8080')
