import dash
import os
from dash import dcc, html, Input, Output, dash_table
import plotly.express as px
import pandas as pd

def create_dash_app(server):
    dash_app = dash.Dash(
        __name__, 
        server=server, 
        url_base_pathname='/dash/',
        external_stylesheets=[
            "https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css",
            "https://fonts.googleapis.com/css2?family=Roboto:wght@400;700&display=swap",
            "https://cdn.tailwindcss.com"
        ]
    )

    file_path = os.path.join(os.path.dirname(__file__), 'static', 'Cleaned_School_DataSet.csv')
    df = pd.read_csv(file_path)

    dash_app.layout = html.Div([
        html.Div([
            dcc.Dropdown(
                id='region-dropdown',
                options=[{'label': region, 'value': region} for region in df['Region'].unique()],
                placeholder="Select a region",
                className="w-3/4 mx-auto p-2 border border-gray-300 rounded-md shadow-sm"
            ),

            dcc.Dropdown(
                id='school-dropdown',
                placeholder="Select a school",
                className="w-3/4 mx-auto p-2 border border-gray-300 rounded-md shadow-sm mt-4"
            ),

            # Data table
            html.Div([
                dash_table.DataTable(
                    id='school-table',
                    columns=[{"name": col, "id": col} for col in ["School Name", "Region", "Province", "Municipality"]],
                    page_size=10,
                    filter_action="native",
                    sort_action="native",
                    style_table={'overflowX': 'auto', 'margin': '0 auto'},
                    style_cell={'textAlign': 'left', 'padding': '10px', 'fontSize': '14px'},
                    style_header={'backgroundColor': '#333', 'color': 'white', 'fontWeight': 'bold'}
                ),
            ], className="w-3/4 mx-auto mt-6"),

            html.Div([
                dcc.Graph(id='enrollment-bar-chart')
            ], className="w-3/4 mx-auto mt-6"),

            html.Div(id='school-details', className="w-3/4 mx-auto mt-6 p-4 bg-white shadow-md rounded-md")
        ], className="max-w-3xl mx-auto bg-white p-6 shadow-lg rounded-md")
    ], className="bg-gray-100 min-h-screen flex items-center justify-center")

    @dash_app.callback(
        Output('school-dropdown', 'options'),
        Input('region-dropdown', 'value')
    )
    def update_schools(region):
        filtered_df = df if not region else df[df['Region'] == region]
        return [{'label': school, 'value': school} for school in filtered_df['School Name'].unique()]

    @dash_app.callback(
        [Output('school-table', 'data'),
         Output('enrollment-bar-chart', 'figure'),
         Output('school-details', 'children')],
        [Input('school-dropdown', 'value')]
    )
    def update_dashboard(selected_school):
        if not selected_school:
            return [], px.bar(title='Select a school to view enrollment'), ""

        school_df = df[df['School Name'] == selected_school]
        table_data = school_df[["School Name", "Region", "Province", "Municipality"]].to_dict('records')

        grade_cols = [col for col in df.columns if col.startswith(('K ', 'G'))]
        enrollment_sums = school_df[grade_cols].sum()
        enrollment_fig = px.bar(
            x=enrollment_sums.index, y=enrollment_sums.values,
            labels={'x': 'Grade Level', 'y': 'Total Enrollment'},
            title=f'Total Student Enrollment for {selected_school}',
            color_discrete_sequence=['#3498db']
        )

        details = html.Div([
            html.H3(selected_school, className="text-xl font-bold"),
            html.P(f"Region: {school_df.iloc[0]['Region']}", className="text-gray-700"),
            html.P(f"Province: {school_df.iloc[0]['Province']}", className="text-gray-700"),
            html.P(f"Municipality: {school_df.iloc[0]['Municipality']}", className="text-gray-700"),
            html.P(f"Total Enrollment: {enrollment_sums.sum()}", className="text-gray-700 font-semibold")
        ])

        return table_data, enrollment_fig, details

    return dash_app
