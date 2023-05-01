from flask import Flask, render_template
from flask_socketio import SocketIO, emit
import pigpio
from pigpio_dht import DHT11
from time import sleep
import threading

BUTTON_GPIO_PIN = 20
LED_GPIO_PIN = 21
DHT11_PIN = 5
sensor = DHT11(DHT11_PIN)
sidste_temp = None

pi_button = pigpio.pi()
pi_led = pigpio.pi()

app = Flask(__name__)
socketio = SocketIO(app)

"""------funktioner-Button-------"""

def tilstand():
    button_state = pi_button.read(BUTTON_GPIO_PIN)
    socketio.emit('button_state', button_state)

@socketio.on('connect')
def connect():
    tilstand()

def cbf(gpio, level, tick):
    tilstand()

pi_button.callback(BUTTON_GPIO_PIN, pigpio.EITHER_EDGE, cbf)

"""-------funktioner-PWM--------"""

@socketio.on('skru_fra_browser')
def skru(data):
    lysstyrke = int(data['lysstyrke'])
    if lysstyrke < 0:
        lysstyrke = 0
    if lysstyrke > 255:
        lysstyrke = 255
    pi_led.set_PWM_dutycycle(LED_GPIO_PIN, lysstyrke)

"""------DHT11-------"""
@socketio.on('hent_temp')
def hent_temp():
    sleep(0.5)
    socketio.emit('temp', sidste_temp)

"""------flask-------"""

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/oevelse3/")
def site1():
    return render_template("oevelse3.html", tilstand=pi_button.read(BUTTON_GPIO_PIN))

@app.route("/oevelse4/")
def site2():
    return render_template("oevelse4.html")

@app.route("/oevelse5/")
def site3():
    return render_template("oevelse5.html")    
def read_temp():
    global sidste_temp
    while True:
        sleep(2)
        try:
            sidste_temp = sensor.read()
        except:
            sidste_temp = None

temp_thread = threading.Thread(target=read_temp)
temp_thread.start()

if __name__ == ('__main__'):
    app.run(host="0.0.0.0", debug=True)