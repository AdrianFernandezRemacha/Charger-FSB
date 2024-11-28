import dash
import dash_bootstrap_components as dbc


app = dash.Dash(external_stylesheets=[dbc.themes.BOOTSTRAP], use_pages=True)

app.layout = dash.html.Div([
    dbc.Navbar([

                dash.html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(dash.html.Img(src="assets/fsb_round_logo.png", height="50px")),
                            dbc.Col(dbc.NavbarBrand("Formula Student Bizkaia", className="ms-2", style={'height' : '56px'})),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    href="https://fsbizkaia.com",
                    style={"textDecoration": "none"},
                ),
                # dbc.NavbarToggler(id="navbar-toggler", n_clicks=0),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("SHARE POINT", href="https://fsbizkaia.sharepoint.com/_layouts/15/sharepoint.aspx", style={'color': 'white'}, target="_blank")))),
                dbc.NavItem(dbc.NavLink(dbc.NavItem(dbc.NavLink("EXCEL IDs", href="https://fsbizkaia.sharepoint.com/:x:/t/fsbmembers/ERifJ4D8R8xOrCAO3HAcln8BEPNhegThUZQlMB3Fv0ZmlA?e=vuEqge&CID=27c39e7c-b294-fbb1-c446-8a4769cf8a29", style={'color': 'white'}, target="_blank"))))
            ],
        color="dark",
        dark=True,
        style={'height': '50px', 'weight': '100%'}  # Ajustar la altura del navbar

    ),

        dash.page_container

    ],
    className="body"
)

if __name__ == '__main__':
    app.run_server(debug=True)
