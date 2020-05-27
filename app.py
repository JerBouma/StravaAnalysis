import webview
from threading import Thread
import json
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

app = dash.Dash(__name__)
app.title = "StravaAnalyser"
server = app.server

with open("Data/General Data/activities_list.json", "r") as read_file:
    activities_list = json.load(read_file)

output = []
for label in activities_list.keys():
    output.append({'label': label, 'value': activities_list[label]})

app.layout = html.Div([
    html.Div([
        html.Summary('Activities'),
        dcc.Dropdown(
            id="selection",
            options=output,
            multi=True)], style={'padding-top': '10px'}, className="two columns"),

    html.Div([
        html.Div(id="graph")], className="ten columns")
])

@app.callback(
    Output(component_id='graph', component_property='children'),
    [Input(component_id="selection", component_property='value')])
def create_graph_of_heartrate(selection):
    data = {}

    for activity_id in selection:
        with open("Data/Streams Data/" + activity_id + ".json", "r") as read_file:
            data[activity_id] = json.load(read_file)

    traces = []
    for activity in data:
        title = next(item for item in output if item["value"] == activity)['label']
        scatter = {'x': data[activity]['time'], 'y': data[activity]['heartrate'], 'name': title}
        traces.append(scatter)

    graph = dcc.Graph(
        id='stock_data_graph',
        figure={'data': traces})

    return graph

if __name__ == '__main__':
    # def run_app():
    #     app.run_server(debug=False)
    #
    # t = Thread(target=run_app)
    # t.daemon = True
    # t.start()
    #
    # window = webview.create_window('StravaAnalyser', 'http://127.0.0.1:8050/')
    # webview.start(  debug=True)
    app.run_server(debug=True)