from flask import Flask
import pigpio

pi = pigpio.pi()
app = Flask(__name__)

BUTTON_GPIO_PIN = 20

@app.route('/')
def index():
    if pi.read(BUTTON_GPIO_PIN) == 0:
        return 'TRYKKET'
    else:
        return 'SLUPPET'

if __name__ == '__main__':
    app.run(host="0.0.0.0")
