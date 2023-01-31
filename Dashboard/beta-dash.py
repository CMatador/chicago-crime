import dash
from dash import dcc, html
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

#always use this to start
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.SOLAR])

con = pymssql.connect(server, username, password, database)

image1_path = 'assets/ml1.png'
image2_path = 'assets/ml2.png'
image3_path = 'assets/ml3.png'

df4 = pd.read_csv('clara.csv')
df5 = pd.read_csv('safety-scores.csv')
df6 = pd.read_csv('correlation.csv')
df7 = pd.read_csv('miscon_crimes.csv')

fig4 = px.bar(df5, x='School_Survey_Safety', y='count_of_scores', color = 'Primary_Category', text_auto=True, title='Count of Student Responses to Safety Survey', opacity=1, height=485)

fig5 =  px.scatter(df4, x = 'Graduation_Rate_School', y = 'num_crimes', trendline = 'ols', width=720,
 labels={"Graduation_Rate_School": "School Graduation Rates",
         "num_crimes": "Number of Crimes"},
 title = 'Graduation Rates vs. Number of Crimes in Ward Area (2022)')

# fig6 = px.imshow(df4.corr(),
# #  x=df4.columns,
# #  y=df4.columns,
#  color_continuous_scale = 'pubugn',
#  title='Number of Crimes x Student Demographics', text_auto = '.2f',aspect='auto')

fig7 = px.imshow(
    df6.corr(),
    color_continuous_scale = 'RdBu_r',
    range_color = [-1,1],
    labels=dict(color='correlation'),
    width=720,
    height=560,
    text_auto = '.2f',
    aspect='auto', 
)

fig7.update_xaxes(side='top')

fig8 = px.imshow(
    df7.corr(),
    color_continuous_scale = 'RdBu_r',
    range_color = [-1,1],
    labels=dict(color='correlation'),
    width=720,
    height=560,
    text_auto = '.2f',
    aspect='auto',
)

fig8.update_xaxes(side='top')


#########################################################################################################################################################################################
query3 = f"SELECT primary_type as Type_of_Crime, year, domestic, count(domestic) as Count_of_Domestic_Crimes from {table} WHERE year < 2023 AND domestic = 1 GROUP BY primary_type, domestic, year"
df3 = pd.read_sql(query3, con)

fig3 = px.line(df3, x='year', y='Count_of_Domestic_Crimes', color='Type_of_Crime', markers=True, title='Domestic Crimes in Chicago',  height=600)


#########################################################################################################################################################################################

query2 = f"SELECT primary_type as Type_of_Crime, year, count(primary_type) as Count_of_Crimes from {table} WHERE year < 2023 GROUP BY primary_type, year"
df2 = pd.read_sql(query2, con)

fig2 = px.line(df2, x='year', y='Count_of_Crimes', color= 'Type_of_Crime', markers=True, title='Crime in Chicago From 2013 to 2022', height=600)

#########################################################################################################################################################################################

query1 = f"SELECT primary_type as Type_of_Crime, LEFT(date, 6) as date, latitude, longitude from {table} WHERE year = 2023"
df1 = pd.read_sql(query1, con)

fig1 = px.scatter_mapbox(df1, lat= 'latitude', lon= 'longitude', hover_name= "Type_of_Crime", hover_data= ["date"], color= 'Type_of_Crime', color_discrete_sequence=px.colors.qualitative.Dark24, title="Map of Crimes in Chicago (2023)", zoom=9, height=650, width=950)
fig1.update_layout(mapbox_style="open-street-map")
fig1.update_traces(marker=dict(size=8))

#put figures into dashboard's html
app.layout = html.Div(children=[
    html.H1(children='Crime and Education in Chicago'),

    html.Div(children='''
        Examining Crime and its Possible Effects on Education and Students in Chicago Public Schools.
    '''),


    dcc.Graph(
        id='first-graph',
        figure=fig1
    ),

    dcc.Graph(
            id='second-graph',
            figure=fig2
    ),

    dcc.Graph(
            id='third-graph',
            figure=fig3
    ),

    dcc.Graph(
            id='fourth-graph',
            figure=fig4,
    ),

    dcc.Graph(
            id='fifth-graph',
            figure=fig5
    ),

    # dcc.Graph(
    #         id='sixth-graph',
    #         figure=fig6
    # ),

    dcc.Graph(
            id='seventh-graph', figure=fig7, style={'display': 'inline-block'},
    ),
    html.Div(className='spacer'),

    dcc.Graph(
            id='eighth-graph', figure=fig8, style={'display': 'inline-block'}, 
    ), 

    html.Img(src=image1_path, id='nine'),
    html.Img(src=image2_path, id="ten"),
    html.Img(src=image3_path, id='eleven'),

])

#run the app
if __name__ == '__main__':
    app.run_server(debug=True)
