import requests
from bs4 import BeautifulSoup
from datetime import datetime
from pytz import timezone

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output
from dash_table import DataTable

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

tz = timezone("America/Detroit")
now = lambda: datetime.now(tz)
ptime = lambda time, form: datetime.strptime(time, form).time()
ftime = lambda string, form: datetime.strftime(string, form)

def menu(hall):
    link = url + hall.replace(' ', '-')

    # stores entire page's HTML in variable soup
    r = requests.get(link)
    soup = BeautifulSoup(r.content, 'html5lib')

    # gets mealtimes as time objects
    spans = soup.findAll('span', attrs = {'class':'calhours-times'})
    pairs = [span.string.replace('\xa0', ' ').split(' ‑ ') for span in spans]
    times = [[ptime(x, '%I:%M %p')for x in pair] for pair in pairs]

    # fallback returns
    foods = 'Closed'
    hours = 'Closed'

    # checks if any meal is open
    boos = [start <= now().time() <= end for start, end in times]

    # gets foods for open meal
    if any(boos):
        ind = boos.index(True)
        hours = pairs[ind][1]

        # gets divs for all meals
        divs = soup.find_all('div', attrs = {'class': 'courses'})

        try:
            meal = divs[ind].find_all('div', attrs = {'class': 'item-name'})
            foods = ', '.join([food.getText().strip() for food in meal])
        except:
            foods = 'Error'
            hours = 'Error'

    return {
        'Hall': hall,
        'Closing': hours,
        'Foods': foods,
    }

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
# app.title = 'M|Dining Scraper'

app.layout = html.Div([
    html.H1('M|Dining Foods'),
    html.H3('What can I eat right now?'),

    html.Button('Find out!', id='button'),
    html.Br(),
    html.Br(),

    html.Div(id='timestamp', children='Updated: '),

    DataTable(
        id='table',
        columns=[
            dict(
                id=x,
                name=x,
            )
            for x in ['Hall', 'Closing', 'Foods']
        ],
        style_cell = dict(textAlign = 'left'),
    ),

    html.Br(),
    html.Br(),
    html.H3('Where is the food I want?'),
    html.Label('In the "filter data..." box, type the food\'s name capitalized and press enter'),

    html.Div([
        DataTable(
            id='index',
            columns=[
                dict(
                    id=x,
                    name=x,
                )
                for x in ['Food', 'Hall', 'Closing']
            ],

            style_cell = dict(textAlign = 'left'),
            filter_action="native",
            page_action="native",
            page_current= 0,
            page_size= 10,
        ),
    ], className='two columns')
])

@app.callback(
    [
        Output('table', 'data'),
        Output('timestamp', 'children')
    ],
    [
        Input('button', 'n_clicks')
    ]
)
def update(clicks):
    return [
        [menu(hall) for hall in halls],
        'Updated: ' + ftime(now(), '%I:%M %P')
    ]

@app.callback(
    [
        Output('index', 'data'),
    ],
    [
        Input('table', 'data'),
    ]
)
def search(data):
    return [
        [
            {
                'Food': food,
                'Hall': row['Hall'],
                'Closing': row['Closing']
            }
            for row in data
            for food in row['Foods'].split(', ')
        ],
    ]

if __name__ == '__main__':
    app.run_server()
