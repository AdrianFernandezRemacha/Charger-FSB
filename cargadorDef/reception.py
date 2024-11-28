import os
os.environ['KVDLLPATH'] = r'C:\Program Files\Kvaser\Drivers'
from canlib import canlib, Frame, exceptions
import json
import time


dictionary = {
    #id Brusa   
    "18ff50e5": "0000000000000000", # la del cargador
    "1806e5f4": "0000000000000000", # la que manda el master
    #id Master
    "0310": "0000010000000000",
    "0311": "0000000000000000",
    #id popUps
    "0000":"00",
    #id temps con NIT 0
    "010d":"0000000000000000",
    "010e":"0000000000000000",
    "010f":"0000000000000000",
    "0110":"0000000000000000",
    "0111":"0000000000000000",
    "0112":"0000000000000000",
    "0113":"0000000000000000",
    "0114":"0000000000000000",
    "0115":"0000000000000000",
    "0116":"0000000000000000",
    "0117":"0000000000000000",
    "0118":"1500000000000000",
    #id temps con NIT 1
    "110d":"0010000000000000",
    "110e":"0000000000000000",
    "110f":"0000000000000000",
    "1110":"0000000000000000",
    "1111":"0000000000000000",
    "1112":"0000000000000000",
    "1113":"0000000000000000",
    "1114":"0000000000000000",
    "1115":"0000000000000000",
    "1116":"0000000000000000",
    "1117":"0000000000000000",
    "1118":"0000000000000000",
    #id voltages con NIT 0
    "0100": "0000000000000000",
    "0101": "0000000000000000",
    "0102": "0000000000000000",
    "0103": "0000000000000000",
    "0104": "0000000000000000",
    "0105": "0000000000000000",
    "0106": "0000000000000000",
    "0107": "0000000000000000",
    "0108": "3b00000000000000",
    "0109": "0000000000000000",
    "010a": "0000000000000000",
    "010b": "0000000000000000",
    #id voltages con NIT 1
    "1100": "0000000000000000",
    "1101": "003b000000000000",
    "1102": "0000000000000000",
    "1103": "0000000000000000",
    "1104": "0000000000000000",
    "1105": "0000000000000000",
    "1106": "0000000000000000",
    "1107": "0000000000000000",
    "1108": "0000000000000000",
    "1109": "0000000000000000",
    "110a": "0000000000000000",
    "110b": "0000000000000000"
}

nit = {
    #id temps con NIT 1
    "010d":"0000000000000000",
    "010e":"0000000000000000",
    "010f":"0000000000000000",
    "0110":"0000000000000000",
    "0111":"0000000000000000",
    "0112":"0000000000000000",
    "0113":"0000000000000000",
    "0114":"0000000000000000",
    "0115":"0000000000000000",
    "0116":"0000000000000000",
    "0117":"0000000000000000",
    "0118":"1500000000000000",
    #id voltages con NIT 1
    "0100": "0000000000000000",
    "0101": "0000000000000000",
    "0102": "0000000000000000",
    "0103": "0000000000000000",
    "0104": "0000000000000000",
    "0105": "0000000000000000",
    "0106": "0000000000000000",
    "0107": "0000000000000000",
    "0108": "3b00000000000000",
    "0109": "0000000000000000",
    "010a": "0000000000000000",
    "010b": "0000000000000000",
}

class Reception:
    def __init__(self) -> None:
        while True:
            try:
                self.ch_a = canlib.openChannel(0)
                self.ch_a.setBusParams(canlib.canBITRATE_500K)
                self.ch_a.busOn()
                break
            except canlib.exceptions.CanNotFound:
                dictionary.update({"0000" : "01"})
                with open("data.json", "w") as outfile:
                    json.dump(dictionary, outfile)
            time.sleep(90)

    def escribir(self):
        try:   
            msg = self.ch_a.read(timeout=250)
            if msg.flags != canlib.canMSG_ERROR_FRAME:                                              #esto no he comprobado si funciona
                dictionary.update({"0000" : "00"})
                
                id = str(hex(int(msg.id))).split('x')[-1].zfill(4)                                  #id con el siguiente formato '000'
                data = str(msg.data.hex())                                                          #data con el siguiente formato '0000000000000000'
                if id in nit and data[-1]=='1':                                                     #para generar todas las ids de temperaturas y voltajes con nit=1
                            id = '1' + id[1:]

                dictionary.update({id : data})                                                      #actualizar diccionario                 
                with open("data.json", "w") as outfile:                                             #dumpear diccionario en el json.data
                    json.dump(dictionary, outfile)
            else:                                                   
                print(msg)                                                                          # printear mensaje
                print(msg.flags)                                                                    # printear error
                dictionary.update({"0000" : "02"})                                                  # error 5
                with open("data.json", "w") as outfile:             
                    json.dump(dictionary, outfile)                                                  # mandar error

        except canlib.exceptions.CanNoMsg:
            dictionary.update({"0000" : "02"})                  
            with open("data.json", "w") as outfile:
                json.dump(dictionary, outfile)
        
        except canlib.exceptions.CanGeneralError:
            dictionary.update({"0000" : "03"})                  
            with open("data.json", "w") as outfile:
                json.dump(dictionary, outfile)

def main():
    recept = Reception()
    while True:
        recept.escribir()

if __name__ == '__main__':
    main()