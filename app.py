import json
import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output, State
import dash_auth
from pandas.io.json import json_normalize
import importlib
insta = importlib.import_module("instagram-locations")

# read credentials from file
with open('config', 'r') as cred:
    CREDENTIALS = cred.read().split(',')

# create dash app with basic auth
app = dash.Dash(__name__)
auth = dash_auth.BasicAuth(app, {CREDENTIALS[0]: CREDENTIALS[1]})
server = app.server

# base map from examples list on github
userMap = open('./docs/map.html', 'r').read()

# define app layout
app.layout = html.Div([html.H1('search-by-location'),
                       html.Div([
                           html.Label('Enter sessionid:  '),
                           dcc.Input(value="3888090946%3AhdKd2fA8d72dqD%3A16", type='string'
                                      , id='sessionid', size = 40,
                                     style={"margin-left": "2px"})
                        ]),
                        html.Div([
                           html.Label('Enter latitude:  '),
                            dcc.Input(value=32.22, type='number', id='latitude',
                                      style={"margin-left": "13px"})
                        ]),
                        html.Div([
                           html.Label('Enter longitude:  '),
                            dcc.Input(value=-110.97, type='number', id='longitude')
                        ]),
                        html.Div([
                           html.Label('Enter Date:  '),
                            dcc.Input(value="2020-06-09", type='date', id='user_date'
                                      , style={"margin-left": "31px"})
                        ]),
                       html.Div([
                            html.Button('Submit', id='submit-val', n_clicks=0)
                       ]),
                        dcc.Loading(
                                    id="loading-1",
                                    type="default",
                                    children=[html.Label(id="loading-output")]
                        ),
                        html.Div([
                            html.Button("Download CSV", id="btn_csv", style={"margin-top": "10px"}),
                            dcc.Download(id="download-loc"),
                            dcc.Store(id='location-val')
                        ]),
                        html.Iframe(id='user_map', srcDoc=userMap, width='90%', height='500')
                       ])

# add a callback to cache location data based on user button interaction.
@app.callback(
    [Output(component_id='loading-output', component_property='children'),
    Output(component_id='location-val', component_property='data')],
    [Input(component_id='submit-val', component_property='n_clicks')],
    [State(component_id='sessionid', component_property='value'),
    State(component_id='latitude', component_property='value'),
    State(component_id='longitude', component_property='value'),
    State(component_id='user_date', component_property='value')],
    prevent_initial_call=True,)
def create_map(n_clicks, sessionid, latitude, longitude, user_date):
    cookie = 'sessionid=' + sessionid
    print(sessionid, latitude, longitude, user_date,)
    try:
        locations = insta.get_fuzzy_locations(float(latitude), float(longitude), cookie)
        return_code = "Updated for: {} | {} | {} | {}".format(sessionid, latitude, longitude, user_date)
    except KeyError:
        print("ERROR: KeyError whilst accessing location data.")
        return_code = "KeyError - Refresh sessionid: {} ".format(sessionid)
        locations = None
    return return_code, locations


# add a callback to build the map.
@app.callback(
    Output(component_id='user_map', component_property='srcDoc'),
    [Input(component_id='location-val', component_property='data')],
    [State(component_id='sessionid', component_property='value'),
     State(component_id='latitude', component_property='value'),
     State(component_id='longitude', component_property='value'),
     State(component_id='user_date', component_property='value')],
    prevent_initial_call=True,)
def create_map(locations, sessionid, latitude, longitude, user_date):
    if locations is None:
        return None
    else:
        template = insta.Template(insta.html_template)
        date_var = ''
        if user_date is not None:
            date_var = '?max_id=' + insta.encode_date(user_date)
        viz = template.substitute(lat=latitude, lng=longitude, locs=json.dumps(insta.make_geojson(locations)), date_var=date_var)
        user_map = open('map.html', 'w')
        user_map.write(viz)
        user_map.close()
        user_map = open('map.html', 'r').read()
        return user_map

# add a callback to download location data as csv
@app.callback(
    Output(component_id="download-loc", component_property="data"),
    [Input(component_id="btn_csv", component_property="n_clicks"),
     State(component_id='location-val', component_property='data')],
    prevent_initial_call=True,
)
def download(n_clicks, locations):
    try:
        df = json_normalize(locations)
        return dcc.send_data_frame(df.to_csv, "output.csv")
    except ValueError:
        error_msg = "ERROR: Dataframe empty. Check location is not None due to sessionid error."
        return dict(content=error_msg, filename="error.txt")

if __name__ == "__main__":
    app.run_server(debug=False)