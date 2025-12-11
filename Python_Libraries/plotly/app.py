import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Data
df = pd.DataFrame({
    'Actor': ['Leonardo Dicaprio','Leonardo Dicaprio','Leonardo Dicaprio',
              'Jake Gyllenhaal','Jake Gyllenhaal','Jake Gyllenhaal',
              'Christian Bale','Christian Bale','Christian Bale',
              'Brad Pitt','Brad Pitt','Brad Pitt'],
    'Movie': ['The Revenant','Inception','The Wolf of Wall Street',
              'Prisoners','Zodiac','Nightcrawler',
              'American Psycho','Ford vs Ferrari','The Dark Knight',
              'Fight Club','SE7EN','F1'],
    'Year': [2015, 2010, 2013,
             2013, 2007, 2014,
             2000, 2019, 2008,
             1999, 1995, 2009],
    'Genre': ['Adventure','Sci-Fi','Biography',
              'Thriller','Crime','Thriller',
              'Horror','Drama','Action',
              'Drama','Thriller','Action'],
    'Rating': [8.0, 8.8, 8.2,
               8.1, 7.7, 7.8,
               7.6, 8.1, 9.0,
               8.8, 8.6, 7.1],
    'BoxOffice': [533000000, 829000000, 392000000,
                  122000000, 84000000, 87000000,
                  34000000, 117000000, 1005000000,
                  101000000, 327000000, 25000000]
})

# Initialize Dash app
app = dash.Dash(__name__)

# Layout
app.layout = html.Div([
    html.H1("Interactive Movie Dashboard"),

    html.Label("Select Actor:"),
    dcc.Dropdown(
        id='actor-dropdown',
        options=[{'label': actor, 'value': actor} for actor in df['Actor'].unique()],
        value='Leonardo Dicaprio', clearable=False
    ),

    html.Label("Minimum Rating:"),
    dcc.Slider(
        id='rating-slider',
        min=df['Rating'].min(),
        max=df['Rating'].max(),
        step=0.1,
        value=df['Rating'].min(),
        marks={i:str(i) for i in range(int(df['Rating'].min()), int(df['Rating'].max())+1)}
    ),

    dcc.Graph(id='scatter-graph'),
    dcc.Graph(id='bar-graph')
])

# Callback to update charts
@app.callback(
    [Output('scatter-graph', 'figure'),
     Output('bar-graph', 'figure')],
    [Input('actor-dropdown', 'value'),
     Input('rating-slider', 'value')]
)
def update_charts(selected_actor, min_rating):
    filtered_df = df[(df['Actor']==selected_actor) & (df['Rating']>=min_rating)]
    
    scatter_fig = px.scatter(filtered_df, x='Rating', y='BoxOffice', size='BoxOffice',
                             hover_data=['Movie','Genre'], title=f'{selected_actor} Movies')
    
    bar_fig = px.bar(filtered_df, x='Movie', y='BoxOffice', color='Genre',
                     title=f'BoxOffice of {selected_actor} Movies')
    
    return scatter_fig, bar_fig

# Run app (Dash v3+)
if __name__ == '__main__':
    app.run(debug=True)
