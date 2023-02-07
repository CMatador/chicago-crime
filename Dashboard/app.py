import dash
from dash import dcc, html, callback, Output, Input
import plotly.express as px
import pandas as pd
import sqlalchemy
import sqlite3
from plotly._subplots import make_subplots
import plotly.graph_objects as go
import dash_bootstrap_components as dbc

import pymssql
from config import database
from config import table
from config import username
from config import password
from config import server

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

con = pymssql.connect(server, username, password, database)


query1 = f"SELECT primary_type as Type_of_Crime, LEFT(date, 6) as date, latitude, longitude from {table} WHERE year = 2023"
df1 = pd.read_sql(query1, con)

fig1 = px.scatter_mapbox(df1, lat= 'latitude', lon= 'longitude', hover_name= "Type_of_Crime", hover_data= ["date"], color= 'Type_of_Crime', color_discrete_sequence=px.colors.qualitative.Dark24, labels={'Type_of_Crime': 'Type of Crime'}, title="Crimes in Chicago (2023)", zoom=9, height=650, width=950)
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_traces(marker=dict(size=8))

query2 = f"SELECT primary_type as Type_of_Crime, year, count(primary_type) as Count_of_Crimes from {table} WHERE year < 2023 GROUP BY primary_type, year"
df2 = pd.read_sql(query2, con)

fig2 = px.line(df2, x='year', y='Count_of_Crimes', color= 'Type_of_Crime', markers=True, labels={"year": "Year", 'Count_of_Crimes': 'Count of Crimes', 'Type_of_Crime': 'Type of Crime'}, title='Crime in Chicago From 2013 to 2022', height=600)

query3 = f"SELECT primary_type as Type_of_Crime, year, domestic, count(domestic) as Count_of_Domestic_Crimes from {table} WHERE year < 2023 AND domestic = 1 GROUP BY primary_type, domestic, year"
df3 = pd.read_sql(query3, con)

fig3 = px.line(df3, x='year', y='Count_of_Domestic_Crimes', color='Type_of_Crime', markers=True, labels={"year": "Year", 'Count_of_Domestic_Crimes': 'Count of Domestic Crimes', 'Type_of_Crime': 'Type of Crime'}, title='Domestic Crimes in Chicago From 2013 to 2022',  height=600)

df4 = pd.read_csv('dash-csv/clara.csv')
df5 = pd.read_csv('dash-csv/safety-scores.csv')
df6 = pd.read_csv('dash-csv/correlation.csv')
df7 = pd.read_csv('dash-csv/miscon_crimes.csv')

fig4 = px.histogram(df5, x='School_Survey_Safety', color = 'Primary_Category', labels={"School_Survey_Safety": "School Safety Survey Responses", 'Primary_Category': 'Category of School', 'count': 'Count of School Safety Scores'}, text_auto=True, title='Count of Student Responses to Safety Survey', height=500)
fig4.update_layout(bargap=0.3)

fig5 =  px.scatter(df4, x = 'Graduation_Rate_School', y = 'num_crimes', trendline = 'ols',
 labels={"Graduation_Rate_School": "School Graduation Rates",
         "num_crimes": "Number of Crimes"},
 title = 'Graduation Rates vs. Number of Crimes in Ward Area (2022)')

fig6 = px.imshow(
    df6.corr(),
    color_continuous_scale = 'RdBu_r',
    range_color = [-1,1],
    labels=dict(color='correlation'),
    width=720,
    height=560,
    text_auto = '.2f',
    aspect='auto', 
)

fig6.update_xaxes(side='top')

fig7 = px.imshow(
    df7.corr(),
    color_continuous_scale = 'RdBu_r',
    range_color = [-1,1],
    labels=dict(color='correlation'),
    width=720,
    height=560,
    text_auto = '.2f',
    aspect='auto',
)

fig7.update_xaxes(side='top')

fig8 = px.scatter(df7, x = '# of Misconducts', y= 'num_crimes', trendline='ols', labels={"num_crimes": "Number of Crimes"}, title= 'Number of Misconducts vs. Number of Crimes in Ward Area (2022)')
fig9 = px.scatter(df7, x = '# of Suspensions (includes ISS and OSS)', y= 'num_crimes', trendline='ols', labels={"num_crimes": "Number of Crimes"}, title= 'Number of Suspensions vs. Number of Crimes in Ward Area (2022)')
fig10 = px.scatter(df7, x = '# of Police Notifications', y = 'num_crimes', trendline='ols', labels={"num_crimes": "Number of Crimes"}, title = 'Number of Police Notifications vs. Number of Crimes in Ward Area (2022)')

image1_path = 'assets/ml1.png'
image2_path = 'assets/ml2.png'
image3_path = 'assets/ml3.png'











SIDEBAR_STYLE = {
    "position": "fixed",
    "top": 0,
    "left": 0,
    "bottom": 0,
    "width": "16rem",
    "padding": "2rem 1rem",
    "background-color": "#B3DDF2",
}

CONTENT_STYLE = {
    "margin-left": "18rem",
    "margin-right": "2rem",
    "padding": "2rem 1rem",
}

sidebar = html.Div(
    [
        html.H2("Topics", className="display-4"),
        html.Hr(),
        html.P("Click on each topic to find relevant visuals related to each topic.", className="lead"),
        dbc.Nav(
            [
                dbc.NavLink("Home", href="/", active="exact"),
                dbc.NavLink("Crime in Chicago", href="/page-1", active="exact"),
                dbc.NavLink("Education", href="/page-2", active="exact"), 
                dbc.NavLink("Machine Learning", href="/page-3", active="exact"),
            ],
            vertical=True,
            pills=True,
        ),
    ],
    style=SIDEBAR_STYLE
)

content = html.Div(id="page-content", style=CONTENT_STYLE)

app.layout = html.Div([dcc.Location(id="url"), sidebar, content])

@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        return html.H1(children='Crime and Education in Chicago', style={'textAlign': 'center', 'marginTop': 30, 'marginBotton': 30}), html.H2(children="Examining Crime and its Possible Effects on Education and Students in Chicago Public Schools.", style={'textAlign': 'center', 'marginTop': 25, 'marginBotton': 25}), html.H3(children="Infamously known as 'Chiraq', Chicago's reputation as a violent, crime-infested city precedes it. But is crime in Chicago truly that concerning? This project explores crime in Chicago by analyzing crime statistics to understand crime trends in Chicago. Concurrently, we explore any effects that crime rates and violence in Chicago can have on the state of education and the behaviors of students in Chicago Public Schools.", style={'textAlign': 'center', 'font-weight': 'normal', 'marginTop': 20, 'marginBotton': 20}), html.H3(children="Presented by Law and Order: SQL - Chris Kusha, Clara McGrath, Albert Prouty, Jassleen Bhullar", style={'textAlign': 'center', 'font-weight': 'normal', 'marginTop': 15, 'marginBotton': 15})
    elif pathname == "/page-1":
        return html.H2("Has crime in Chicago increased or decreased over the last decade?"), dcc.Graph(id='first-graph', figure=fig1), dcc.Graph(id='second-graph', figure=fig2), dcc.Graph(id='third-graph', figure=fig3)
    elif pathname == "/page-2":
        return html.H2("What effect has crime in Chicago had on the safety, academic performance, and behavior of students?"), dcc.Graph(id='fourth-graph', figure=fig4), dcc.Graph(id='fifth-graph', figure=fig5), html.H6(children='Correlations Between Misconducts and Police Notifications in Chicago Public Schools', style={'textAlign': 'left', 'font-weight': 'normal'}), dcc.Graph(id='sixth-graph', figure=fig6), dcc.Graph(id='seventh-graph', figure=fig8), dcc.Graph(id='eighth-graph', figure=fig9), dcc.Graph(id='ninth-graph', figure=fig10), html.H6(children='Correlations Between Student Incivilities and Crime in Chicago', style={'textAlign': 'left', 'font-weight': 'normal'}), dcc.Graph(id='tenth-graph', figure=fig7)
    elif pathname == "/page-3":
        return html.H2("Are there any connections between students’ demographics and the reported misconducts?"), html.H4(children=([html.Br(), 'Model: XGBRegressor', html.Br(), 'R-Squared: 0.978', html.Br(), 'Mean Cross-Val Score: 0.89', html.Br(), 'Root Mean Square Error: 82.32']), style={'textAlign': 'left', 'font-weight': 'normal'}), html.Img(src=image1_path, id='nine'), html.Img(src=image2_path, id="ten"), html.Img(src=image3_path, id='eleven')

if __name__ == '__main__':
    app.run_server(debug=True)   