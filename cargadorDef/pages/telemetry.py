import dash_daq as daq
import dash
import dash_bootstrap_components as dbc
from dash import html, callback, Output, Input, dcc
from dash import Dash, html, Input, Output, dcc, ctx, callback
from JSONReader import get_data
import interfaceUpdater as act
import plotly.graph_objs as go
import os
os.environ['KVDLLPATH'] = r'C:\Program Files\Kvaser\Drivers'    # esto arregla un error raro
from canlib import canlib, Frame, exceptions
import json

slaves = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
values = [0, 1, 0, 1, 0, 1, 0, 1, 0, 1, 0, 1]


# abrir canal para mandar CAN
try:
   ch_a = canlib.openChannel(0)                            
   ch_a.busOn()
except canlib.exceptions.CanNotFound:
   dataPopUps = '01'

# inicializaciones
tempsArray = [0 for i in range(144)]                    # estas listas aqui solo tienen 0, se usan para declarar los graficos en el html
voltajesArray = [0 for i in range(144)]                 # si se quiere hacer alguna eragiketa usar estas mismas variables declaradas dentro de interfaceUpdater.py
voltajesPrueba= [0 for i in range(144)]  
tempsPrueba=[0 for i in range(144)]  

dash.register_page(__name__)
layout = html.Div(id='element-to-hide', style={'display':'none'}),\
        html.Div(
            children=[
            dcc.Interval(
                id='int-component',
                interval=125,                                           # in milliseconds
                n_intervals=0
            ),
        ],
    ),\
    html.Div(
        children=[
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.StopButton(
                                        id='stop',
                                        label='Stop charging',
                                        n_clicks=0,         # esto sobra, pero por si acaso probar
                                        size=120,
                                        style={'font-weight': 'bold', 'font-size':'16px', 'text-align':'center'}
                                    )
                            ),
                            html.Div(
                                children=daq.PowerButton(
                                        id='botonDeReset',
                                        on=False,
                                        label='Reset',
                                        size=50,
                                        color='red',
                                        style={'font-weight': 'bold', 'font-size':'16px', 'text-align':'center'}
                                )
                            ),
                            html.Div(
                                children=daq.PowerButton(
                                        id='precharge',
                                        on=False,
                                        label='Precharge',
                                        size=50,
                                        color='red',
                                        style={'font-weight': 'bold', 'font-size':'16px', 'text-align':'center'}
                                )
                            ),
                            html.Div(
                                children=daq.PowerButton(
                                        id='startCharging',
                                        on=False,
                                        label='Start Charging',
                                        size=50,
                                        color='red',
                                        style={'font-weight': 'bold', 'font-size':'16px', 'text-align':'center'}
                                )
                            )
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=[html.H5('Sent Current',
                                        style={'font-weight': 'bold', 'font-size':'16px', 'text-align':'center'}
                                    ),
                                    dcc.Slider(0, 10, 1, # min, max, step
                                        value=0,
                                        id='meterCorriente',
                                        className="sliderCurrent"
                                    )
                            ]),
                            html.Div(
                                children=daq.LEDDisplay(
                                    id='current3',
                                    label={'label':"Hall sensor", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                    labelPosition='top',
                                    value='0',
                                    color="black",
                                    size=30
                                )
                            )
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.Indicator(
                                            id='k13',
                                            label={'label':"K1+", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="green",
                                            value=True,
                                            size=40
                                            
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                            id='k23',
                                            label={'label':"K2+", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="green",
                                            value=True,
                                            size=40 
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                            id='k33',
                                            label={'label':"K3-", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="green",
                                            value=True,
                                            size=40
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                            id='estadoDeseado',
                                            label={'label':"desired", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="green",
                                            value=True,
                                            size=40
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                            id='estadoReal',
                                            label={'label':"real", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="green",
                                            value=True,
                                            size=40
                                )
                            )
                        ],
                        className="subcontainerGitano"
                    ),
                ],
                className="subcontainer5"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMinTemp3',
                                        label={'label':"Min Temp", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",  
                                        size=30  
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='idCellMinTemp3',
                                        label={'label':"ID", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                    )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMaxTemp3',
                                        label={'label':"Max Temp", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='idCellMaxTemp3',
                                        label={'label':"ID", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                    )
                            )    
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMinVoltage3',
                                        label={'label':"Min Voltage", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='3.64',
                                        color="black",
                                        size=30                 # el tamaño en pixeles
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='idCellMinVoltage3',
                                        label={'label':"ID", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='cellMaxVoltage3',
                                        label={'label':"Max Voltage", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='idCellMaxVoltage3',
                                        label={'label':"ID", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30  
                                )
                            )
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.LEDDisplay(
                                        id='totalVoltage3',
                                        label={'label':"Total Voltage (V)", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        labelPosition='top',
                                        value='0',
                                        color="black",
                                        size=30
                                )
                            ),
                            html.Div(
                                children=[html.H5('AMS State Machine',
                                        style={'font-weight': 'bold','font-size':'16px', 'text-align':'center'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='smAMS3',
                                        style={'font-size':'16px', 'text-align':'center'}
                                        ),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}
                            ),
                            html.Div(                                        
                                children=[html.H5('AMS Error',
                                        style={'font-weight': 'bold','font-size':'16px', 'text-align':'center'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='errorAMS3',
                                        style={'font-size':'16px', 'text-align':'center'}
                                        ),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}
                            ),
                            html.Div(
                                children=[html.H5('AMS Mode',
                                        style={'font-weight': 'bold','font-size':'16px', 'text-align':'center'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='modeAMS3',
                                        style={'font-size':'16px', 'text-align':'center'}
                                        ),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}
                            )
                        ],
                        className="subcontainer6"
                    )
                ],
                className="subcontainer5"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.LEDDisplay(
                                    id='voltageBrusaE5',
                                    label={'label':"Brusa Voltage", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                    labelPosition='top',
                                    value='0',
                                    color="black",
                                    size=30
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                    id='currentBrusaE5',
                                    label={'label':"Brusa Current", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                    labelPosition='top',
                                    value='0',
                                    color="black",
                                    size=30
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                        id='errorBrusaE5',
                                        label={'label':"BrusaError", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        color="red",
                                        size=40,
                                        value=True
                                )
                            ),
                            html.Div(
                                children=[html.H5('Brusa Status',
                                    style={'font-weight': 'bold','font-size':'16px', 'text-align':'center'}
                                    ),
                                    html.H5('Waiting for data',
                                    id='statusBrusaE5',
                                    style={'font-size':'16px', 'text-align':'center'}
                                    ),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}
                            ), 
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.LEDDisplay(
                                    id='voltageLimitAms',
                                    label={'label':"Voltage Limit", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                    labelPosition='top',
                                    value='0',
                                    color="black",
                                    size=30
                                )
                            ),
                            html.Div(
                                children=daq.LEDDisplay(
                                    id='currentAms',
                                    label={'label':"AMS Current", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                    labelPosition='top',
                                    value='0',
                                    color="black",
                                    size=30
                                )
                            ),
                            html.Div(
                                children=daq.Indicator(
                                        id='chargerStateAms',
                                        label={'label':"Charging", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                        color="red",
                                        size=40,
                                        value=True
                                )
                            ),
                            html.Div(
                                children=html.Img(
                                    src='/assets/logo.jpg',  
                                    style={'width': '100px', 'height': '100px'}  # Ajusta el tamaño según sea necesario
                                )
                            )
                        ],
                        className="subcontainer6"
                    ),
                    html.Div(
                        children=[
                            html.Div(
                                children=daq.Indicator(
                                            id='ams3',
                                            label={'label':"AMS", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="red",
                                            size=40,
                                            value=True
                                )
                            ),
                             html.Div(
                                children=daq.Indicator(
                                            id='imd3',
                                            label={'label':"IMD", 'style':{'font-weight': 'bold','font-size':'16px', 'text-align':'center'}},
                                            color="red",
                                            size=40,
                                            value=True
                                )
                            ),
                            html.Div(
                                children=[html.H5('Timed Out Slave',
                                        style={'font-weight': 'bold','font-size':'16px', 'text-align':'center'}
                                        ),
                                        html.H5('Waiting for data',
                                        id='timedOutSlave3',
                                        style={'font-size':'16px', 'text-align':'center'}
                                        ),
                                ],
                                style={'display': 'flex', 'align-items': 'center', 'flex-direction': 'column'}
                            )
                        ],
                        className="subcontainer6"
                    )
                ],
                className="subcontainer5"
            ),
            html.Div(
                children=[
                    html.Div(
                        children=[dcc.Graph(
                            id = 'temps',
                            style={'height': 300},
                            figure = go.Figure(data=[go.Scatter(x=[i for i in range(len(tempsPrueba))], y=tempsPrueba)]) #,mode='markers',
                            )
                        ]
                    ),
                    html.Div(
                        children=[dcc.Graph(
                            id = 'voltajes',
                            style={'height': 300}, 
                            figure = go.Figure(data=[go.Scatter(x=[i for i in range(len(voltajesPrueba))], y=voltajesPrueba)]),
                            config={'displayModeBar': False},
                            )
                        ]
                    )
                ],
                className="subcontainer4",
                style={'grid-gap': '10px', 'align-items': 'start', 'width': 'auto', 'margin': '0', 'padding': '0'}
                
            ), 
            html.Div(                                                           # pop-up,
                children=dbc.Modal(
                    [
                        dbc.ModalHeader(dbc.ModalTitle("ERROR")),
                        dbc.ModalBody("Waiting for data",id='error'),
                    ],
                    id="popUp",
                    is_open=False,
                    size="lg",
                    backdrop="static"
                )
            ) 
        ],
        className="contenedor5"
    )                                      

@callback(
    # En output están todos los valores que se quieres actualizar, definiendo en cada uno la "id" del elemento y su "atributo a actualizar"
    [Output('error','children'),
    Output('popUp','is_open'),
    Output("voltajes","figure"),                                
    Output("temps","figure"),                                   
    Output("botonDeReset","on"),                                
    Output("startCharging", "on"),                              
    Output("precharge", "on"),                   
    Output('smAMS3', 'children'), 
    Output('errorAMS3', 'children'), 
    Output('modeAMS3', 'children'), 
    Output('timedOutSlave3', 'children'),
    Output('cellMinVoltage3', 'value'), 
    Output('cellMaxVoltage3', 'value'), 
    Output('idCellMaxVoltage3', 'value'), 
    Output('idCellMinVoltage3', 'value'), 
    Output('cellMinTemp3', 'value'), 
    Output('cellMaxTemp3', 'value'), 
    Output('idCellMinTemp3', 'value'), 
    Output('idCellMaxTemp3', 'value'), 
    Output('totalVoltage3', 'value'), 
    Output('current3', 'value'), 
    Output('k13', 'color'), 
    Output('k23', 'color'), 
    Output('k33', 'color'), 
    Output('cellMinVoltage3', 'color'), 
    Output('cellMaxTemp3', 'color'), 
    Output('imd3', 'color'), 
    Output('ams3', 'color'),
    Output('voltageBrusaE5', 'value'),
    Output('currentBrusaE5', 'value'),
    Output('statusBrusaE5', 'children'),
    Output('errorBrusaE5', 'color'),
    Output('voltageLimitAms', 'value'),
    Output('currentAms', 'value'),
    Output('chargerStateAms', 'color'),
    Output('estadoDeseado', 'color'),
    Output('estadoReal', 'color'),
    ],
    [Input('int-component', 'n_intervals'),                               # por todos estos inputs se va a ejecutar el callback ## n = cada cuanto se actualiza
    Input('botonDeReset', 'on'),                                         
    Input('startCharging', 'on'),                                        
    Input('precharge', 'on'),                                            
    Input('meterCorriente', 'value'),                                    
    Input('stop', 'n_clicks'),                                           
    Input('error', 'children'),                                           
    Input('popUp', 'is_open')                                             
    ],
)
def acutaliza(N, botonDeReset, startDeCharging, botonDeprecharge, valorCorriente, botonStop, prevPopUpError, prepPopUpState):
    # mensajes de CAN recibidos
    data = dict(get_data())

    # id de popUps errors
    dataPopUps = data.get('0000')
    
    # mandar mensajes de CAN
    dataPopUps, nuevoBotonReset, nuevoBotCharging, nuevoBotonPrecharge = mandarCan(dataPopUps, botonDeReset, startDeCharging, botonDeprecharge, valorCorriente, ctx.triggered_id == 'stop', data.get('0310'))                                                          
    
    # actualizar temps, voltajes y corriente(la corriente solo se actualiza no se manda)
    nuevoTempsFigure = act.tempsNuevas(data)
    nuevoVoltajesFigure = act.voltajesNuevos(data)

    # actualizar brusa (feedback del cargador mandado por el AMS)
    voltageBrusaE5, currentBrusaE5, statusBrusaE5, errorBrusaE5 = act.brusaFeedback(data.get("18ff50e5"))   # id del cargador
    voltageLimitAms, currentAms, chargerStateAms = act.amsCargadorFeedback(data.get("1806e5f4"))            # id que manda el master

    # actualizar el resto de datos
    totalVoltage, minVoltage, idMinVoltage, voltageColor, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp = act.updateVoltages(data.get('0311'))
    k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed, estado_deseado, estado_real  = act.contactorFeedbackAndAMSState(data.get('0310'),data.get("18ff50e5"))
    
    # actualizar estado popups
    error, popUp = act.actualizaPopUp(dataPopUps, prevPopUpError, prepPopUpState)

    # mantener el mismo orden de las variables que hay en el outPut
    return error, popUp, nuevoVoltajesFigure, nuevoTempsFigure, nuevoBotonReset, nuevoBotCharging, nuevoBotonPrecharge, smAMS, errorAMS, amsMode, timedOutSlvave, minVoltage, maxVoltage, idMaxVoltage, idMinVoltage, minTemp, maxTemp, idMinTemp, idMaxTemp, totalVoltage, current, k1, k2, k3, voltageColor, colorTemp, imd, amsLed, voltageBrusaE5, currentBrusaE5, statusBrusaE5, errorBrusaE5, voltageLimitAms, currentAms, chargerStateAms, estado_deseado, estado_real

#//////////////////////////////////////////////////////////////////////////////////////////////////////////////////

def mandarCan(dataPopUps, botonDeReset, startDeCharging, botonDeprecharge, valorCorriente, botonStop, data):
    stateAms = str(data[0:2])                                                           # estado del ams
    carState = str(data[8:10])                                                          # estado del coche

    nuevoBotonReset = False  
    nuevoBotonPrecharge = False                               
    nuevoBotCharging = False
    charging = 0
    state = 0

    if carState =="00":                                                                 # modo cargador
        if stateAms == '07'or stateAms == '08' or stateAms == '09':                     # 7 error reseteable, 8 critical error, 9 charge end reseteable                   
            nuevoBotonPrecharge = False                                                 # precarga y charging a 0
            nuevoBotCharging = False                        
            state = 0
            charging = 0
            if (stateAms == '07' or stateAms == '09') and botonDeReset:                 # y el boton de reset solo se puede pulsar cuando estemos en estado 7 o 9
                nuevoBotonReset = True
                state = 1
        elif botonDeprecharge and (not startDeCharging):                                # Mandar precarga
            nuevoBotonPrecharge = True
            state = 2    
            charging = 0        
        elif startDeCharging and botonDeprecharge:                                      # Boton de charging solo cuando esta dado 
            state = 2
            nuevoBotonPrecharge = True
            if valorCorriente !=0:
                nuevoBotCharging = True
                charging = 1
            else:
                nuevoBotCharging = False
                charging = 0
           
        dataPopUps = write(dataPopUps, Frame(id_ = 99, data = [state, 00, charging, 00, 00, 00, 00, int(10 * valorCorriente)]))             # la id esta en decimal, en hexadecimal es la 63
    else:            
        dataPopUps = write(dataPopUps, Frame(id_ = 105, data = [1, 00, 00, 00 ,00 ,00, 00, 00]))                                            # la id esta en decimal, en hexadecimal es la 69

    if botonStop:                                                                 # STOP: Boton de precarga y charging a 0
            charging = 0
            nuevoBotCharging = False
            state = 0
            nuevoBotonPrecharge = False
    
    return dataPopUps, nuevoBotonReset, nuevoBotCharging, nuevoBotonPrecharge

def write(dataPopUps, msg):
    try:
        ch_a.write(msg)
    except canlib.exceptions.CanOverflowError:
        dataPopUps = '04'                           
    except canlib.exceptions.CanGeneralError:                               # una vez enchufado y lo desconectas
        dataPopUps = '03'                          
    except NameError:
        dataPopUps = '01'
    return dataPopUps
        
