from flask import Flask
from flask import redirect
import pigpio

pi = pigpio.pi()
app = Flask(__name__)
LED_GPIO_PIN = 21

@app.route('/on')
def on():
    pi.write(LED_GPIO_PIN, 1)
    return redirect('/')
    

@app.route('/off')
def off():
    pi.write(LED_GPIO_PIN, 0)
    return redirect('/')

@app.route('/')
def index():
    return str(pi.read(LED_GPIO_PIN)) + '<a href="/on">Tænd</a><a href="/off">Sluk</a>'
    
if __name__ == '__main__':
    app.run(host="0.0.0.0")
