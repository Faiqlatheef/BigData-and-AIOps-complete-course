import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine

app = dash.Dash(__name__)

def fetch_data():
    engine = create_engine('mysql+mysqlconnector://root:@localhost/task')
    query = "SELECT * FROM sales"
    df = pd.read_sql(query, engine)
    return df

app.layout = html.Div([
    dcc.Interval(
        id='interval-component',
        interval=1*3600*1000,  # in milliseconds (1 hour)
        n_intervals=0
    ),
    dcc.Graph(id='bar-chart'),
    dcc.Graph(id='line-chart'),
    dcc.Graph(id='pie-chart'),
    dcc.Graph(id='scatter-plot'),
    dcc.Graph(id='histogram'),
    dcc.Graph(id='box-plot'),
    dcc.Graph(id='area-chart'),
    dcc.Graph(id='funnel-chart'),
    dcc.Graph(id='sunburst-chart'),
    dcc.Graph(id='treemap-chart')
])

@app.callback(
    [Output('bar-chart', 'figure'),
     Output('line-chart', 'figure'),
     Output('pie-chart', 'figure'),
     Output('scatter-plot', 'figure'),
     Output('histogram', 'figure'),
     Output('box-plot', 'figure'),
     Output('area-chart', 'figure'),
     Output('funnel-chart', 'figure'),
     Output('sunburst-chart', 'figure'),
     Output('treemap-chart', 'figure')],
    [Input('interval-component', 'n_intervals')]
)
def update_charts(n):
    df = fetch_data()

    bar_fig = px.bar(df, x='product_name', y='sale_amount')
    line_fig = px.line(df, x='sale_date', y='sale_amount')
    pie_fig = px.pie(df, values='sale_amount', names='product_name')
    scatter_fig = px.scatter(df, x='sale_date', y='sale_amount', color='product_name')
    hist_fig = px.histogram(df, x='sale_amount')
    box_fig = px.box(df, x='product_name', y='sale_amount')
    area_fig = px.area(df, x='sale_date', y='sale_amount')
    funnel_fig = px.funnel(df, x='product_name', y='sale_amount')
    sunburst_fig = px.sunburst(df, path=['product_name'], values='sale_amount')
    treemap_fig = px.treemap(df, path=['product_name'], values='sale_amount')

    return bar_fig, line_fig, pie_fig, scatter_fig, hist_fig, box_fig, area_fig, funnel_fig, sunburst_fig, treemap_fig

if __name__ == '__main__':
    app.run_server(debug=True)
