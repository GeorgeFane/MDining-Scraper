import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

from dash import Dash
import dash_html_components as html
from dash_table import DataTable

url = 'https://dining.umich.edu/menus-locations/dining-halls/'
halls = ["Bursley", "East Quad", "Markley", "Mosher-Jordan", "North Quad", "South Quad", "Twigs at Oxford"]

tz = timezone("America/Detroit")
now = lambda: datetime.now(tz)
ptime = lambda time, form: datetime.strptime(time, form).time()
ftime = lambda string, form: datetime.strftime(string, form)

def menu(hall):
    link = url + hall.replace(' ', '-')

    # stores entire page's HTML in soup
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')

    # gets mealtimes as time objects
    spans = soup.findAll('span', attrs = {'class':'calhours-times'})
    pairs = [span.string.replace('\xa0', ' ').split(' ‑ ') for span in spans]
    times = [[ptime(x, '%I:%M %p')for x in pair] for pair in pairs]

    # fallback returns
    foods = 'Closed'
    hours = 'Closed'

    # gets divs for all meals
    divs = soup.find_all('div', attrs = {'class': 'courses'})

    # checks if any meal is open
    boos = [start <= now().time() <= end for start, end in times]

    # gets foods for open meal
    if any(boos):
        ind = boos.index(True)
        hours = pairs[ind][1]
    
        meal = divs[ind].find_all('div', attrs = {'class': 'item-name'})
        foods = ', '.join([food.getText().strip() for food in meal])

    return {
        'Hall': hall,
        'Closing': hours,
        'Foods': foods,
    }

headers = ['Hall', 'Closing', 'Foods']
data = [menu(hall) for hall in halls]

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('MDining Foods'),
    html.H3('Updated ' + ftime(now(), '%I:%M %p')),

    DataTable(
        id='table',
        columns=[
            dict(
                id=x,
                name=x,
            )
            for x in headers
        ],
        data = data,
        style_cell = dict(textAlign = 'left'),
    ),
])

if __name__ == '__main__':
    app.run_server()
