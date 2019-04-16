import dash
from dash.dependencies import Input, Output, State
import dash_core_components as dcc
import dash_html_components as html

import datetime
import pandas_datareader.data as web

app = dash.Dash()

app.layout = html.Div(children=[
    html.H1(children="Financial time series"),
    html.Div(children='''
        Let's make a graph for stock price!
    '''),

    dcc.Input(id="input", value="Enter something", type="text"),
    html.Button(id="button", children="Submit"),
    html.Div(id="output-graph")
])

@app.callback(
    Output(component_id="output-graph", component_property="children"),
    [Input(component_id="button", component_property="n_clicks")],
    [State(component_id="input", component_property="value")]
)
def update_value(n_clicks, value):
    input_data = str(value)+".HK"
    print(input_data)
    try:
        start = datetime.datetime(2018, 1, 1)
        end = datetime.datetime.now()
        df = web.DataReader(input_data, "av-daily", start, end,
                            access_key="19BE06QQHG6EXLXV")#os.getenv('ALPHAVANTAGE_API_KEY'))

        df.reset_index(inplace=True)
        df.rename(columns={"index": "date"}, inplace=True)

        return  dcc.Graph(
            id="Price of "+input_data,
            figure={
                "data": [
                    {"x": df.date, "y": df.close, "type": "line", "name": input_data}
                ],
                "layout": {
                    "title": input_data
                }
            }
        )
    except:
        return dcc.Graph()

if __name__ == '__main__':
    app.run_server(debug=True)
