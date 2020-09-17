import requests 
from bs4 import BeautifulSoup 

def scrape(link):
    r = requests.get(link) 
    
    soup = BeautifulSoup(r.content, 'html.parser') 

    table = soup.find('div', attrs = {'id':'content'}) 
    titles=table.findAll('span', attrs = {'class':'calhours-title'})
    times=table.findAll('span', attrs = {'class':'calhours-times'})
    
    return {title.string: time.string.replace('\xa0', ' ') for title, time in zip(titles, times)}

url='https://dining.umich.edu/menus-locations/dining-halls/'

halls=["Bursley","East Quad","Markley","Mosher-Jordan","North Quad","South Quad","Twigs at Oxford"]

links=[url+hall.replace(' ', '-') for hall in halls]

def getTable():
    headers=[]
    rows=[scrape(link) for hall, link in zip(halls, links)]
    
    for row, hall in zip(rows, halls):
        headers+=row.keys()
        row['Hall']=hall

    return set(headers), rows

headers, data=getTable()

from datetime import datetime
from pytz import timezone
tz = timezone("America/Detroit")
now=lambda: datetime.now(tz).strftime("%m/%d/%Y, %H:%M:%S")

from dash import Dash
import dash_core_components as dcc
import dash_html_components as html

from dash.dependencies import Input, Output, State
from dash_table import DataTable

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

app.layout = html.Div([
    html.H1('MDining Hours'),
    html.H3('Updated '+now()),

    DataTable(
        id='table',
        columns=[
            dict(
                id=x,
                name=x,
            )
            for x in headers
        ],
        data=data,

        sort_action="native",
        sort_mode="multi",
        page_action="native",
	    
        style_as_list_view=True,
    ),
])
	
if __name__ == '__main__':
    app.run_server()
