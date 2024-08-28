from dash import Dash, dcc, html, page_container
import dash_bootstrap_components as dbc

print('Initializing app')
app = Dash(__name__, use_pages=True, external_stylesheets=[dbc.themes.SLATE])

navbar = dbc.Navbar(
    dbc.Container(
        [
            dbc.NavbarBrand("CDC BRFSS Survey Dashboard", href="/"),
            dbc.Nav(
                [
                    dbc.NavItem(dbc.NavLink("Homepage", href="/")),
                    dbc.NavItem(dbc.NavLink("Overview", href="/overview")),
                    dbc.NavItem(dbc.NavLink("Demographics", href="/demographics")),
                    dbc.NavItem(dbc.NavLink("Lifestyle", href="/lifestyle")),
                    dbc.NavItem(dbc.NavLink("Health Conditions", href="/health_conditions")),
                    dbc.NavItem(dbc.NavLink("CDC BRFSS Website", href="https://www.cdc.gov/brfss/annual_data/annual_data.htm", target="_blank")),
                    dbc.DropdownMenu(
                        children=[
                            dbc.DropdownMenuItem("More", header=True),
                            dbc.DropdownMenuItem("Surveys", href="https://www.cdc.gov/brfss/questionnaires/index.htm", target="_blank"),
                            dbc.DropdownMenuItem("More Trends", href="https://www.cdc.gov/brfss/brfssprevalence/index.html", target="_blank")
                        ],
                        nav=True,
                        in_navbar=True,
                        label="More",
                    ),
                ],
                className="ml-auto",
                navbar=True,
            ),
        ]
    ),
    color="dark",
    dark=True,
    sticky="top",
)

footer = dbc.Container(
    dbc.Row(
        [
            dbc.Col(
                dbc.Button("Home", href='/', color='primary', className='mr-2'),
                align='left',
                width='auto'
            ),
            dbc.Col(
                dbc.Button("Back to Top", href='#', color='secondary', className='mr-2'),
                align='center',
                width='auto'
            ),
            dbc.Col(
                html.A("GitHub", href='/'),
                align='right',
                width='auto'
            )
        ],
        justify='between'  # Space out columns evenly
    ),
    className='footer',
    fluid=True
)

app.layout = html.Div([
    navbar,
    page_container,
    footer,
])

def run_dash_app():
    print('Running app on server')
    app.run_server(port=8050, debug=True)

if __name__ == '__main__':
    run_dash_app()