import pandas as pd
import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Create app
app = dash.Dash(__name__)

# Clear the layout and suppress exceptions until the callback is executed
app.config.suppress_callback_exceptions = True

# Read the wildfire data into pandas dataframe
df = pd.read_csv(
    'https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/Historical_Wildfires.csv')

# Extract year and month from the date column
df['Month'] = pd.to_datetime(df['Date']).dt.month_name()  # Month names
df['Year'] = pd.to_datetime(df['Date']).dt.year

# Fix typo in accessing unique regions
region_list = df['Region'].unique()

# Layout Section of Dash
app.layout = html.Div([
    # Title
    html.H1('Australia Wildfire Dashboard',
            style={'textAlign': 'center', 'color': '#503D36', 'font-size': 26}),

    # Outer division
    html.Div([
        # Region selection (radio items)
        html.Div([
            html.H2('Select Region:', style={'margin-right': '2em'}),
            dcc.RadioItems(
                [{"label": "New South Wales", "value": "NSW"},
                 {"label": "Northern Territory", "value": "NT"},
                 {"label": "Queensland", "value": "QL"},
                 {"label": "South Australia", "value": "SA"},
                 {"label": "Tasmania", "value": "TA"},
                 {"label": "Victoria", "value": "VI"},
                 {"label": "Western Australia", "value": "WA"}],
                value="NSW", id='region', inline=True
            )
        ]),

        # Year selection (dropdown)
        html.Div([
            html.H2('Select Year:', style={'margin-right': '2em'}),
            dcc.Dropdown(
                options=[{"label": year, "value": year} for year in sorted(df['Year'].unique())],
                value=2005, id='year'
            )
        ]),

        # Two empty divisions for the output graphs
        html.Div([
            html.Div([], id='plot1'),
            html.Div([], id='plot2')
        ], style={'display': 'flex', 'justify-content': 'space-between', 'margin-top': '20px'})
    ])
])


# Callback for updating the plots
@app.callback(
    [Output('plot1', 'children'),
     Output('plot2', 'children')],
    [Input('region', 'value'),
     Input('year', 'value')]
)
def reg_year_display(input_region, input_year):
    # Filter data by region and year
    region_data = df[df['Region'] == input_region]
    y_r_data = region_data[region_data['Year'] == input_year]

    # Plot 1: Monthly Average Estimated Fire Area
    est_data = y_r_data.groupby('Month')['Estimated_fire_area'].mean().reset_index()
    fig1 = px.pie(
        est_data,
        values='Estimated_fire_area',
        names='Month',
        title=f"{input_region}: Monthly Average Estimated Fire Area in {input_year}"
    )

    # Plot 2: Monthly Average Count of Pixels for Presumed Vegetation Fires
    veg_data = y_r_data.groupby('Month')['Count'].mean().reset_index()
    fig2 = px.bar(
        veg_data,
        x='Month',
        y='Count',
        title=f"{input_region}: Average Count of Pixels for Presumed Vegetation Fires in {input_year}"
    )

    return [dcc.Graph(figure=fig1), dcc.Graph(figure=fig2)]


# Run the app
if __name__ == '__main__':
    app.run_server()

