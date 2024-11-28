import plotly.graph_objects as go
import random

tempsArray = [0 for i in range(144)]
voltajesArray = [0 for i in range(144)]

AMSERRORS = {
    '0' : 'OK',
    '1' : 'VLoad',
    '2' : 'Current',
    '4' : 'IMD',
    '8' : 'Error contactores',
    '16' : 'Voltaje',
    '32' : 'Temperatura',
    '64' : 'Timeout error',
    '128' : 'Slaves Timeout'
}

AMSSTATES = {
    '01' : 'Charge waiting',
    '02' : 'Charge precharge',
    '03' : 'Charge charging',
    '04' : 'Car waiting',
    '05' : 'Car precharge',
    '06' : 'Car RTD',
    '07' : 'Error',
    '08' : 'Critical Error',
    '09' : 'Charge End'
}

TIMEDOUTSLAVE = {                       # na asi no
    '1' : 'Slave 1 timeout',
    '2' : 'Slave 1 timeout',
    '4' : 'Slave 1 timeout',
    '8' : 'Slave 1 timeout',
    '16' : 'Slave 1 timeout',
    '32' : 'Slave 1 timeout'
}

def actualizaLEDDisplay(num):
    numero = random.randint(0,10)
    color = 'red' if numero == 5 else 'black'
    tercer_byte = num[-6:-4] # estan en negativo para que el primer byte este a la derecha
    return numero,color

def actualizaFigure(numero):
    figure = go.Figure(data=[go.Scatter(x=[1, 2, 3], y=[numero*4, numero*1, numero*2])])
    figure['layout']['yaxis'] = {'range' : (0,30)}
    return figure

def actualizaPopUp(dato, prevPopUp, prepPopUpState):
    popUp = False
    if dato=='01':                                                                   # como el error es reseteable, no vamos a dejar que el usuario quite el popUp
            error = "Device not connected. Conect it and restart reception.py & app.py"
            popUp = True
    elif dato=='02':
        if prevPopUp=="No message available" and prepPopUpState==False:              # si el usuario ya ha visto el error y lo ha cerrado mantenerlo cerrado
            popUp = False   
            error = "No message available"
        else:                                                                        # mostrar error
            error = "No message available"
            popUp = True
    elif dato=='03':
            error = "Device disconected. Conect it and restart reception.py & app.py"
            popUp = True
    elif dato=='04':                                                                 # como el error es reseteable, no vamos a dejar que el usuario quite el popUp
            error = "CanOverflowError. Restart app.py"
            popUp = True
    elif dato=='05':                                                                 # este caso ya no existe, ahora en caso de bus error va al caso 2, no message available para mejor manejo del usuario con la aplicacion
        if prevPopUp=="Bus errors = Error frames" and prepPopUpState==False:              # si el usuario ya ha visto el error y lo ha cerrado mantenerlo cerrado
            popUp = False   
            error = "Bus errors = Error frames"
        else:                                                                        # mostrar error
            error = "Bus errors = Error frames"
            popUp = True
    if dato =='00':
        error = "No error"
        popUp = False
    return error, popUp

def updateVoltages(data):
    minVoltage = round(float(int(data[0:2], base=16) / 51.0),3)
    totalVoltage = round(sum(voltajesArray),1)
    idMinVoltage = int(data[2:4][0:2], base=16)
    maxVoltage = round(float(int(data[4:6], base=16) / 51.0), 3)
    idMaxVoltage = int(data[6:8][0:2], base=16)
    minTemp = int(data[12:14][0:2], base=16)
    idMinTemp = int(data[14:16][0:2], base=16)
    maxTemp = int(data[8:10][0:2], base=16)
    idMaxTemp = int(data[10:12][0:2], base=16)
    if totalVoltage>532.8:
        colorVoltage='green'
    elif totalVoltage>512:
        colorVoltage='orange'
    else:
        colorVoltage='red'

    if maxTemp<40:
        colorTemp='green'
    elif 60>maxTemp>40:
        colorTemp='orange'
    else:
        colorTemp='red'

    return totalVoltage, minVoltage, idMinVoltage, colorVoltage, maxVoltage, idMaxVoltage, minTemp, idMinTemp, maxTemp, idMaxTemp, colorTemp


def contactorFeedbackAndAMSState(data, dataBrusa):
    contactores = bin(int(data[2:4][0:2], base=16)).split('b')[1].zfill(8)
    # print(f"constactores: {contactores}") 
    k1 = 'green' if contactores[-1] == '1' else 'black' if contactores[-4] == '1' else 'grey'
    k2 = 'green' if contactores[-2] == '1' else 'black' if contactores[-5] == '1' else 'grey'
    k3 = 'green' if contactores[-3] == '1' else 'black' if contactores[-6] == '1' else 'grey'
    # k1_error = True if contactores[-4] == '1' else False
    # k2_error = True if contactores[-5] == '1' else False
    # k3_error = True if contactores[-6] == '1' else False
    estado_real = 'green' if contactores[-7] == '1' else 'grey'
    estado_deseado = 'green' if contactores[-8] == '1' else 'grey'
    smAMS = str(data[0:2][0:2])
    smAMS = AMSSTATES.get(smAMS)
    # amsLed = 'red' if int(data[4:6][0:2], base=16) != 0 else 'grey'
    amsLed = 'red' if smAMS == 'Error' or smAMS == 'Critical Error' else 'grey'             # comprobar si funciona
    errorAMS = str(int(data[4:6][0:2], base=16))                                            # obtener el numero de error
    errorAMS = AMSERRORS.get(errorAMS)                                                      # error en texto
    # if k1_error:
    #     errorAMS + "\n K1+ error"
    # elif k2_error:
    #     errorAMS + "\n K2+ error"
    # elif k3_error:
    #     errorAMS + "\n K3- error"
    imd = 'red' if int(data[6:8][0:2], base=16) == 1 else 'grey'
    amsMode = 'Car' if int(data[8:10][0:2], base=16) == 1 else 'Charger'                     
    dato1 = bin(int(data[12:14], 16))[2:].zfill(6)                          # penultimo byte
    dato2 = bin(int(data[10:12], 16))[2:].zfill(6)                          # antepenultimo byte
    datosCombinados = dato1 + dato2                                         # sumar los dos bytes de forma que el bit con mayor peso queda a la izquierda
    datosCombinados = datosCombinados[::-1]                                 # darle la vuelta para que el bit con mayor peso quede a la derecha
    slaves_fallando_str = ""                            
    for i, bit in enumerate(datosCombinados):                               # añadir los slaves que fallan en un string
        if bit == '1':
            slaves_fallando_str += str(i + 1) + " - "
    timedOutSlvave =  'Slaves: ' + slaves_fallando_str
    # current = round(-200+(1.568*int(data[14:16][0:2], base=16)),1)
    current = float(int(dataBrusa[4:8], 16)) / 10.0
    return k1, k2, k3, smAMS, errorAMS, imd, amsMode, timedOutSlvave, current, amsLed, estado_deseado, estado_real

def brusaFeedback(data):
    voltageBrusa = float(int(data[0:4], 16)) / 10.0
    currentBrusa = float(int(data[4:8], 16)) / 10.0
    errorBrusa = "grey"
    status = ""
    statusData = bin(int(data[8:10], 16)).split("b")[1].zfill(8)                        # En esta columna estan los errores tal cual aparecen en el datasheet
    if statusData[-1] == "1":
        status = "Hardware Failure"                                                     # Hardware Failure
        errorBrusa = "red"
    elif statusData[-2] == "1":
        status = "Over temperature"                                                     # Over temperature protection
        errorBrusa = "red"
    elif statusData[-3] == "1":
        status = "Bad input voltage"                                                    # Input voltage is wrong, the charger will stop working
        errorBrusa = "red"
    elif statusData[-4] == "1":
        status = "Battery not connected"                                                # Battery is not connected or the battery is connected reversely
        errorBrusa = "red"
    elif statusData[-5] == "1":
        status = "Time-out"                                                             # Communication receive time-out                                  
        errorBrusa = "red"
    else:
        status = "All okay"
    return voltageBrusa, currentBrusa, status, errorBrusa

def amsCargadorFeedback(data):
    voltageLimit = float(int(data[0:4], 16)) / 10.0
    current = float(int(data[4:8], 16)) / 10.0
    if data[8:10] == '01':
        state = "grey"
    else:
        state = "green"

    return voltageLimit, current, state
#TEMPERATURAS
def tempsNuevas(data):

    temps = ''
    temps += data.get('010d')[0:14]
    temps += data.get('110d')[0:10]
    temps += data.get('010e')[0:14]
    temps += data.get('110e')[0:10]
    temps += data.get('010f')[0:14]
    temps += data.get('110f')[0:10]
    temps += data.get('0110')[0:14]
    temps += data.get('1110')[0:10]
    temps += data.get('0111')[0:14]
    temps += data.get('1111')[0:10]
    temps += data.get('0112')[0:14]
    temps += data.get('1112')[0:10]
    temps += data.get('0113')[0:14]
    temps += data.get('1113')[0:10]
    temps += data.get('0114')[0:14]
    temps += data.get('1114')[0:10]
    temps += data.get('0115')[0:14]
    temps += data.get('1115')[0:10]
    temps += data.get('0116')[0:14]
    temps += data.get('1116')[0:10]
    temps += data.get('0117')[0:14]
    temps += data.get('1117')[0:10]
    temps += data.get('0118')[0:14]
    temps += data.get('1118')[0:10]

    x=0
    for i in range(len(tempsArray)):
        tempsArray[i]=int(temps[x:x+2],16)
        x=x+2
    

    figureT = go.Figure(data=[go.Scatter(x=[i for i in range(len(tempsArray))], y=tempsArray)],)
    figureT.update_layout(xaxis=dict(
        title='Temperature Sensors',
        tickmode='array',
        tickvals=[i * 12 for i in range(13)],                                   # Esto establece los ticks cada 12 unidades
        ticktext=[str(i * 12) for i in range(13)],                               # Esto establece los textos de los ticks
            
    ))
    
    figureT['layout']['yaxis'] = {'range': (5,80), 'title': 'Temperature (ºC)'}  # para ponerle un rango en el eje 
    figureT.update_traces(line_shape='hv')                                       # para ponerlo modo binario
    figureT.update_layout(
        autosize=False,
        height=300,
        margin=dict(l=70, r=50, t=10, b=1)
    )
    return figureT

# VOLTAJES
def voltajesNuevos(data):
    
    voltaje = ''
    voltaje += data.get('0100')[0:14]
    voltaje += data.get('1100')[0:10]
    voltaje += data.get('0101')[0:14]
    voltaje += data.get('1101')[0:10]
    voltaje += data.get('0102')[0:14]
    voltaje += data.get('1102')[0:10]
    voltaje += data.get('0103')[0:14]
    voltaje += data.get('1103')[0:10]
    voltaje += data.get('0104')[0:14]
    voltaje += data.get('1104')[0:10]
    voltaje += data.get('0105')[0:14]
    voltaje += data.get('1105')[0:10]
    voltaje += data.get('0106')[0:14]
    voltaje += data.get('1106')[0:10]
    voltaje += data.get('0107')[0:14]
    voltaje += data.get('1107')[0:10]
    voltaje += data.get('0108')[0:14]
    voltaje += data.get('1108')[0:10]
    voltaje += data.get('0109')[0:14]
    voltaje += data.get('1109')[0:10]
    voltaje += data.get('010a')[0:14]
    voltaje += data.get('110a')[0:10]
    voltaje += data.get('010b')[0:14]
    voltaje += data.get('110b')[0:10]
    
    x=0
    for i in range(len(voltajesArray)):
        voltajesArray[i]=int(voltaje[x:x+2],16)/51
        x=x+2
    
    figureV = go.Figure(data=[go.Scatter(x=[i for i in range(len(voltajesArray))], y=voltajesArray)])
    figureV.update_layout(xaxis=dict(
        title= 'Voltage Sensors',
        tickmode='array',
        tickvals=[i * 12 for i in range(13)],                               # Esto establece los ticks cada 12 unidades
        ticktext=[str(i * 12) for i in range(13)]                           # Esto establece los textos de los ticks
    ))

    figureV['layout']['yaxis'] = {'range': (3,4.2), 'title':'Voltage (V)'}   # para ponerle un rango en el eje 
    figureV.update_traces(line_shape='hv')                                  # para ponerlo modo binario

    figureV.update_layout(
        autosize=False,
        margin=dict(l=70, r=50, t=0, b=1)
        # minreducedheight=500
    )
   
    return figureV
