import os
import dash
from dash import html, dcc, Input, Output
import dash_bootstrap_components as dbc
import pandas as pd
import plotly.express as px

def create_dash_apps(server):
    dataset_path = 'static/uploads/active_dataset.csv'

    # Check if file exists and is not empty
    if not os.path.exists(dataset_path) or os.path.getsize(dataset_path) == 0:
        print("active_dataset.csv is missing or empty.")
        df = pd.DataFrame(columns=['Region', 'School Name', 'Total Enrollment', 'School Year'])  # empty structure
    else:
        df = pd.read_csv(dataset_path)

    # --- Geographic View ---
    geo_dash = dash.Dash(__name__, server=server, url_base_pathname='/dash/geographic_view/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    geo_dash.title = "Geographic View"

    geo_dash.layout = html.Div([
        html.H3("Geographic Enrollment View"),
        dcc.Dropdown(options=[{'label': r, 'value': r} for r in df['Region'].unique()],
                     id='region-dropdown', placeholder="Select Region"),
        dcc.Graph(id='geo-chart'),
        html.Div(id='geo-summary')
    ])

    @geo_dash.callback(
        Output('geo-chart', 'figure'),
        Output('geo-summary', 'children'),
        Input('region-dropdown', 'value')
    )
    def update_geo_chart(region):
        if not region or df.empty:
            return {}, "No data available."
        filtered = df[df['Region'] == region]
        fig = px.bar(filtered, x='School Name', y='Total Enrollment', title=f"Enrollment in {region}")
        summary = f"Total schools: {len(filtered)} | Total Enrollment: {filtered['Total Enrollment'].sum()}"
        return fig, summary

    # --- Historical View ---
    hist_dash = dash.Dash(__name__, server=server, url_base_pathname='/dash/historical_view/', external_stylesheets=[dbc.themes.BOOTSTRAP])
    hist_dash.title = "Historical View"

    hist_dash.layout = html.Div([
        html.H3("Historical Enrollment Trends"),
        dcc.Dropdown(options=[{'label': y, 'value': y} for y in sorted(df['School Year'].unique())],
                     multi=True, id='year-dropdown', placeholder="Select Year(s)"),
        dcc.Graph(id='hist-chart')
    ])

    @hist_dash.callback(
        Output('hist-chart', 'figure'),
        Input('year-dropdown', 'value')
    )
    def update_hist_chart(years):
        if not years or df.empty:
            return {}
        filtered = df[df['School Year'].isin(years)]
        fig = px.line(filtered.groupby(['School Year'])['Total Enrollment'].sum().reset_index(),
                      x='School Year', y='Total Enrollment', markers=True,
                      title="Year-on-Year Enrollment")
        return fig
