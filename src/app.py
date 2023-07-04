import dash
from dash import html
from dash import dcc
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import psycopg2
from dash.dash_table import DataTable


# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="Demo",
    user="postgres",
    password="jAad0tv!"
)

# Retrieve the data from PostgreSQL
query = "SELECT * FROM marks_table"
table_data = pd.read_sql(query, conn)

app = dash.Dash()
server = app.server

marks_table_component = DataTable(
    id='table',
    columns=[{'name': col, 'id': col} for col in table_data.columns],
    data=table_data.to_dict('records')
)

# Fetch the avocado data
avocado_data = pd.read_csv("C:/Users/suysaxen/OneDrive - Publicis Groupe/Desktop/avocado-updated-2020.csv")

geo_dropdown = dcc.Dropdown(
    id='geo-dropdown',
    options=[{'label': geo, 'value': geo} for geo in avocado_data['geography'].unique()],
    value='New York'
)

graph_component = dcc.Graph(id='price-graph')

app.layout = html.Div(children=[
    html.H1(children='Avocado and Marks Dashboard'),
    marks_table_component,
    geo_dropdown,
    graph_component
])


@app.callback(
    Output(component_id='price-graph', component_property='figure'),
    Input(component_id='geo-dropdown', component_property='value'))
def update_graph(selected_geography):
    filtered_avocado = avocado_data[avocado_data['geography'] == selected_geography]
    line_fig = px.line(filtered_avocado,
                       x='date', y='average_price',
                       color='type',
                       title=f'Avocado Prices in {selected_geography}')
    return line_fig


if __name__ == '__main__':
    app.run_server(debug=True)
