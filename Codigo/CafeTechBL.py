from gpiozero import DistanceSensor, LED, Button, AngularServo, OutputDevice, TonalBuzzer
import time
from threading import Thread, Lock
from queue import Queue
from CafeTechRecetas import recetas
import ctypes
import warnings
import smbus
from LCD1602 import CharLCD1602
from gpiozero.tones import Tone
import RPi.GPIO as GPIO

class LogicaMaquinaCafe:
    def __init__(self):
        # Pines
        self.dataPin = OutputDevice(17)
        self.latchPin = OutputDevice(27)
        self.clockPin = OutputDevice(22)
        self.ledRojo = LED(19)
        self.ledVerde = LED(26)
        self.botonAbajo = Button(12, pull_up=False, bounce_time=0.1)
        self.botonArriba = Button(16, pull_up=False, bounce_time=0.1)
        self.botonSeleccionar = Button(20)
        self.botonIniciar = Button(21)
        self.sensorProximidad = DistanceSensor(echo=24, trigger=23, max_distance=2)
        print(f"Distancia inicial es: {self.sensorProximidad.distance * 100}")
        print(f"Temperatura actual: {self.leerTemperatura()} C")

        # 7 segmentos
        self.num = [0xc0, 0xf9, 0xa4, 0xb0, 0x99, 0x92, 0x82, 0xf8, 0x80, 0x90]

        self.recetas = recetas
        #self.stock = {"agua": 2000, "cafe": 500, "leche": 1000, "chocolate": 500}
        self.stock = {"agua": 15, "cafe": 12, "leche": 1, "chocolate": 0}
        
        self.mostrarDigito(0)
        
        self.lock = Lock()
        self.procesoEnCurso = False
        
        # LCD
        self.lcd1602 = CharLCD1602()
        self.lcd1602.init_lcd()
        self.lcd1602.clear() 
        self.lcd1602.write(0, 0, '  * CafeTech *')
        self.lcd1602.write(0, 1, 'Escoja su bebida')
        
        # define the pins for 74HC595 Bar
        self.dataPinBar   = OutputDevice(5)      # DS Pin of 74HC595(Pin14)
        self.latchPinBar  = OutputDevice(6)      # ST_CP Pin of 74HC595(Pin12)
        self.clockPinBar  = OutputDevice(13)     # CH_CP Pin of 74HC595(Pin11)
        
        self.actualizarBar(0)
        
        # Buzzer
        self.activarSonido("inicio")

    def shiftOut(self, order, val):
        for i in range(8):
            self.clockPin.off()
            if order == "LSBFIRST":
                self.dataPin.value = (val >> i) & 0x01
            else:
                self.dataPin.value = (val << i) & 0x80
            self.clockPin.on()

    def shiftOutBar(self, order, val):      
        for i in range(0,8):
            self.clockPinBar.off()
            if(order == "LSBFIRST"):
                self.dataPinBar.on() if (0x01&(val>>i)==0x01) else self.dataPinBar.off()
            elif(order == "MSBFIRST"):
                self.dataPinBar.on() if (0x80&(val<<i)==0x80) else self.dataPinBar.off()
            self.clockPinBar.on()

    def actualizarBar(self, porcentaje):
        self.latchPinBar.off()
        self.shiftOutBar("MSBFIRST", porcentaje)
        self.latchPinBar.on()
        
    def mostrarDigito(self, digito):
        self.latchPin.off()
        self.shiftOut("MSBFIRST", self.num[digito])
        self.latchPin.on()
        
    def activarSonido(self, evento):
        self.buzzer = TonalBuzzer(25)
        
        tonos = {
            "inicio":       [("E4", 0.15), ("G4", 0.15), ("C5", 0.3)],
            "finalizacion": [("C5", 0.3), ("G4", 0.15), ("E4", 0.15)],
            "desplazar":    [("B3", 0.1)],
            "seleccionar":  [("G4", 0.15), ("C5", 0.2)],
            "pagado":       [("C4", 0.15), ("E4", 0.2), ("G4", 0.15)],
            "error":        [("E3", 0.2), ("C3", 0.15)],
            "calentando":   [("G3", 0.1), ("A3", 0.1), ("B3", 0.1), ("C4", 0.1)],
            "preparando":   [("C4", 0.2), ("E4", 0.2), ("G4", 0.2)],
            "servida":      [("G4", 0.15), ("C5", 0.2), ("E5", 0.2)]
        }

        if evento in tonos:
            for nota, duracion in tonos[evento]:
                try:
                    self.buzzer.play(nota)
                    time.sleep(duracion)
                except ValueError:
                    print(f"Nota fuera de rango: {nota}")
            self.buzzer.stop()
        self.buzzer.close()
            

    def obtenerDistancia(self):
        try:
            return self.sensorProximidad.distance * 100
        except Exception as e:
            print(f"Error obteniendo la distancia: {e}")
            return None
            
    def validarTarjetaAsync(self, callback):
        if self.procesoEnCurso:
            print("Otro proceso en curso.")
            return
            
        def leerTarjeta():
            tiempoInicio = time.time()
            while time.time() - tiempoInicio < 5:
                try:
                    distancia = self.obtenerDistancia()
                    print(f"Distancia del lector de tarjeta es: {distancia}")
                    if distancia is not None and distancia < 5:
                        self.ledVerde.on()
                        time.sleep(3)
                        self.ledVerde.off()
                        self.procesoEnCurso = False
                        callback(True, "Pago exitoso")
                        return
                except Warning as e:
                    warnings.warn(str(e))
                except Exception as ex:
                    print(f"Error leyendo el sensor: {ex}")
                time.sleep(2)
            self.procesoEnCurso = False
            callback(False, "No se detecto tarjeta.")

        self.procesoEnCurso = True
        hiloSensor = Thread(target=leerTarjeta, daemon=True)
        hiloSensor.start()

    def leerTemperatura(self):
        self.lib.readSensor(4, 1)
        return self.lib.getTemperature()
    
    def simularVaso(self):
        servo = AngularServo(18, min_angle=0, max_angle=180)
        cantidadVueltas = 0
        while cantidadVueltas <= 2:
            servo.min()
            time.sleep(0.7)
            servo.mid()
            time.sleep(0.7)
            servo.max()
            time.sleep(0.7)
            cantidadVueltas += 1
        servo.close()

    def iniciarCuentaRegresiva(self):
        totalLeds = 10
        for i in range(10, 0, -1):
            self.mostrarDigito(i - 1)
            bits = (1 << i) - 1
            self.actualizarBar(bits)
            time.sleep(1)
        self.mostrarDigito(0)
        self.actualizarBar(0)

    def prepararCafeAsync(self, tipo, actualizarProgreso, actualizarProgresoTemp, finalizar):
        if self.procesoEnCurso:
            print("Proceso en curso. No se puede iniciar otro.")
            return
            
        def preparar():
            receta = self.recetas[tipo]
            if not self.verificarIngredientes(receta):
                print("Ingredientes disponibles:")
                for ingrediente, cantidad in self.stock.items():
                    print(f"{ingrediente}: {cantidad} ml/gr")
                finalizar(False, "Ingredientes insuficientes")
                self.procesoEnCurso = False
                return

            self.ledRojo.on()
            tiempoInicio = time.time()
            progreso = 0
            
            self.activarSonido("calentando")
            print(f"Lecturas para estabilizar la temperatura")
            temp = self.leerTemperatura()
            print(f"Temperatura: {temp} C")
            time.sleep(0.1)
            temp = self.leerTemperatura()
            print(f"Temperatura: {temp} C")
            time.sleep(0.1)
            temp = self.leerTemperatura()
            print(f"Temperatura: {temp} C")
            time.sleep(0.1)
            
            tiempoInicio = time.time()
            while time.time() - tiempoInicio < 5:
                temp = self.leerTemperatura()
                print(f"Temperatura actual: {temp} C")
                actualizarProgresoTemp(temp)
                time.sleep(0.1)
                if temp >= 23:
                    break
            
            self.ledRojo.off()
            
            if temp < 23:
                finalizar(False, "No se logro alcanzar la temperatura necesaria para preparar su bebida.")
                self.procesoEnCurso = False
                return
                    
            hiloServo = Thread(target=self.simularVaso, daemon=True)
            hiloDisplay = Thread(target=self.iniciarCuentaRegresiva, daemon=True)
            hiloServo.start()
            hiloDisplay.start()

            progreso = 0
            while progreso <= 10:
                actualizarProgreso(progreso * 10, temp)
                time.sleep(1)
                progreso += 1

            hiloServo.join()
            hiloDisplay.join()
            
            for ingrediente, cantidad in receta.items():
                if ingrediente in self.stock:
                    print(f"Actualizando stock {ingrediente}: Actual {self.stock[ingrediente]}, actualizado {self.stock[ingrediente] - cantidad}")
                    self.stock[ingrediente] -= cantidad

            finalizar(True, "Bebida listo")
            self.procesoEnCurso = False

        self.procesoEnCurso = True
        hiloPreparacion = Thread(target=preparar, daemon=True)
        hiloPreparacion.start()

    def leerTemperatura(self):
        dht = DHT(4)
        time.sleep(1) 
        chk = dht.readDHT11()
        return dht.getTemperature()
        
    def verificarIngredientes(self, receta):
        for ingrediente, cantidad in receta.items():
            if ingrediente == "precio":
                continue
            cantidadActual = self.stock.get(ingrediente, 0)
            print(f"Verificando {ingrediente}: requerido {cantidad}, disponible {cantidadActual}")
            if cantidadActual < cantidad:
                return False
        return True

    def actualizarLCD(self, linea1, linea2):
        self.lcd1602.clear()
        self.lcd1602.write(0, 0, linea1)
        self.lcd1602.write(0, 1, linea2)
        
    def conectarBotones(self, interfaz):
        def validarEstadoBtn(action, button):
            def wrapper():
                if button["state"] == "normal":
                    action()
                else:
                    print("Boton deshabilitado. Accion ignorada.")
            return wrapper

        self.botonArriba.when_pressed = validarEstadoBtn(interfaz.subirSeleccion, interfaz.btnSubir)
        self.botonAbajo.when_pressed = validarEstadoBtn(interfaz.bajarSeleccion, interfaz.btnBajar)
        self.botonSeleccionar.when_pressed = validarEstadoBtn(interfaz.seleccionarBebida, interfaz.btnSeleccionar)
        self.botonIniciar.when_pressed = validarEstadoBtn(interfaz.iniciarPreparacion, interfaz.btnIniciar)
        
    def apagarComponentes(self):
        print("Apagando todos los componentes...")
        self.ledRojo.off()
        self.ledVerde.off()
        self.mostrarDigito(0)
        self.dataPin.off()
        self.latchPin.off()
        self.clockPin.off()
        self.dataPinBar.off()
        self.latchPinBar.off()
        self.clockPinBar.off()
        self.sensorProximidad.close()
        self.lcd1602.clear()
        self.activarSonido("finalizacion")
        GPIO.cleanup()
        print("Componentes apagados correctamente.")


class DHT(object):
    def __init__(self,pin):
        self.lib_name = '/usr/lib/libdht.so'
        self.lib = ctypes.CDLL(self.lib_name)
        self.lib.setDHT11Pin.argtypes = [ctypes.c_int]
        self.lib.readSensor.restype = ctypes.c_int
        self.lib.getHumidity.restype = ctypes.c_double
        self.lib.getTemperature.restype = ctypes.c_double
        self.lib.setDHT11Pin(pin) 
        
    #Read DHT sensor, store the original data in bits[] 
    def readSensor(self,pin,wakeupDelay):
        return self.lib.readSensor(pin, wakeupDelay)
        
    #Read DHT sensor, analyze the data of temperature and humidity
    def readDHT11(self):
        return self.lib.readDHT11()
     
    def getHumidity(self):
        return self.lib.getHumidity()
    
    def getTemperature(self):
        return self.lib.getTemperature()
