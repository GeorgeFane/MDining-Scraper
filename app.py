headers, data = ({'Breakfast', 'Dinner', 'Late Night', 'Lunch'},
 [{'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 8:00 pm',
   'Hall': 'Bursley',
   'Late Night': '8:00 pm ‑ 10:00 pm',
   'Lunch': '10:30 am ‑ 4:30 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 9:00 pm',
   'Hall': 'East Quad',
   'Lunch': '10:30 am ‑ 4:30 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 8:00 pm',
   'Hall': 'Markley',
   'Lunch': '10:30 am ‑ 2:00 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 9:00 pm',
   'Hall': 'Mosher-Jordan',
   'Lunch': '10:30 am ‑ 4:30 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 9:00 pm',
   'Hall': 'North Quad',
   'Lunch': '10:30 am ‑ 4:30 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 9:00 pm',
   'Hall': 'South Quad',
   'Lunch': '10:30 am ‑ 4:30 pm'},
  {'Breakfast': '7:00 am ‑ 10:30 am',
   'Dinner': '4:30 pm ‑ 8:00 pm',
   'Hall': 'Twigs at Oxford',
   'Late Night': '8:00 pm ‑ 10:30 pm',
   'Lunch': '10:30 am ‑ 2:00 pm'}])

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
