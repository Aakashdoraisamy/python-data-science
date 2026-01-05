import dash
from dash import html, dcc
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import plotly.express as px
from utils import fetch_stock_data, calculate_moving_average, calculate_daily_return

# Top companies to monitor
companies = ['AAPL', 'MSFT', 'AMZN', 'GOOGL', 'TSLA']

# Initialize Dash app with Bootstrap theme
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
app.title = "Professional Stock Market Dashboard"

# Layout
app.layout = dbc.Container([
    
    # Header
    dbc.Row([
        dbc.Col(html.H1("Stock Market Dashboard", className="text-center text-primary mb-4"), width=12)
    ]),

    # Dropdown to select companies
    dbc.Row([
        dbc.Col([
            html.Label("Select Companies:"),
            dcc.Dropdown(
                id='company-dropdown',
                options=[{'label': c, 'value': c} for c in companies],
                value=['AAPL'],
                multi=True
            )
        ], width=6)
    ], className='mb-4'),

    # Cards for basic stats (optional)
    dbc.Row([
        dbc.Col(dbc.Card([
            dbc.CardHeader("Dashboard Info"),
            dbc.CardBody([
                html.P("This dashboard shows real-time stock trends, moving averages, volume, and daily returns.", className="card-text")
            ])
        ]), width=12, className="mb-4")
    ]),

    # Stock closing price + moving average chart
    dbc.Row([
        dbc.Col(dcc.Graph(id='stock-price-line'), width=12)
    ]),

    # Stock volume chart
    dbc.Row([
        dbc.Col(dcc.Graph(id='stock-volume-bar'), width=12)
    ]),

    # Daily returns chart
    dbc.Row([
        dbc.Col(dcc.Graph(id='stock-daily-return'), width=12)
    ])

], fluid=True)


# Callback to update charts dynamically
@app.callback(
    [Output('stock-price-line', 'figure'),
     Output('stock-volume-bar', 'figure'),
     Output('stock-daily-return', 'figure')],
    [Input('company-dropdown', 'value')]
)
def update_graph(selected_companies):
    if not selected_companies:
        selected_companies = ['AAPL']
    
    stock_data = fetch_stock_data(selected_companies)
    
    # Initialize figures
    price_fig = px.line(title="Stock Closing Price Trend")
    volume_fig = px.bar(title="Daily Trading Volume")
    return_fig = px.line(title="Daily Returns (%)")
    
    for company in selected_companies:
        df = stock_data[company]
        
        # Closing price
        price_fig.add_scatter(x=df['Date'], y=df['Close'], mode='lines', name=company)
        # Moving average
        ma = calculate_moving_average(df)
        price_fig.add_scatter(x=df['Date'], y=ma, mode='lines', name=f"{company} MA(20)", line=dict(dash='dot'))
        
        # Volume
        volume_fig.add_bar(x=df['Date'], y=df['Volume'], name=company)
        
        # Daily return
        daily_return = calculate_daily_return(df)
        return_fig.add_scatter(x=df['Date'], y=daily_return, mode='lines', name=company)
    
    # Layout adjustments
    price_fig.update_layout(hovermode='x unified')
    volume_fig.update_layout(hovermode='x unified')
    return_fig.update_layout(hovermode='x unified', yaxis_title="Daily Return (%)")
    
    return price_fig, volume_fig, return_fig


if __name__ == "__main__":
    app.run(debug=True)

