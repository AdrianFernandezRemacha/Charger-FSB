import dash
import dash_bootstrap_components as dbc
from dash import html, Dash, Input, ctx, Output
from dash.exceptions import PreventUpdate

dash.register_page(__name__, path='/')
def layout():
    return html.Div(id="body",
        children=[
            html.Div(
            children=[
                html.Div(
                children=[
                    html.Img(src="../assets/fsb_round_logo.png", className="header-logo"),
                    html.H1(children="Dynacar Log Reader", className="header-title"),
                    html.P(
                        children="Analyze Tecnalia's Dynacar log outputs for Formula Student Bizkaia's Torque Vectoring division.",
                        className="header-description",
                    ),
                ],
                className="header-content"
                )
            ],
            className="header",
        ),
        dbc.Row([
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Live Analysis", className="display-3"),
                            html.Hr(className="my-2"),
                            html.P(
                                "Live telemetry data representation."
                            ),
                            dbc.Button("Open App", id="LiveButton", color="light", outline=True, n_clicks=0 , href=dash.page_registry['pages.telemetry']['path']),
                        ],
                        className="h-100 p-5 text-white bg-secondary rounded-3 card",
                    ),
                    md=6,
                ),
                dbc.Col(
                    html.Div(
                        [
                            html.H2("Data Log Analysis", className="display-3"),
                            html.Hr(className="my-2"),
                            html.P(
                                "Toolset to analyze logs and plot values for data analisis."
                            ),
                            dbc.Button("Open App", id="LogButton", color="secondary", outline=True, n_clicks=0, href=dash.page_registry['pages.telemetry']['path']),
                        ],
                        className="h-100 p-5 bg-light border rounded-3 card",
                    ),
                    md=6,
                )
            ],
            className="align-items-md-stretch margin",
            ),
        ],
    className="body"
    )
"""
@app.callback(
    Output('body', 'children'),
    [Input('LiveButton', 'n_clicks'),
    Input('LogButton', 'n_clicks')],
)
def displayClick(btn1, btn2):
    msg = "None of the buttons have been clicked yet"
    if ctx.inputs.get('LiveButton.n_clicks')!=1 and ctx.inputs.get('LogButton.n_clicks')!=1:
        print("ey")
        raise PreventUpdate
    if "LiveButton" == ctx.triggered_id:
        msg = "Button 1 was most recently clicked"
    elif "LogButton" == ctx.triggered_id:
        return app.getBody()
    print(msg)
    return html.Img(src="assets/fsb_round_logo.png",className="header-logo")
"""

