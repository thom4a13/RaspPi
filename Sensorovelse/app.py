import sqlite3                          # Import the sqlite3 library for working with SQLite databases
import datetime                         # Import the datetime module for working with date and time objects
import RPi.GPIO as GPIO                 # Import the RPi.GPIO library for controlling the Raspberry Pi's GPIO pins
import dht11                            # Import the dht11 library for reading data from the DHT11 temperature and humidity sensor
from time import sleep                  # Import the sleep function from the time module for adding delays in the code
from flask import Flask, render_template # Import the Flask framework for building web applications and the render_template function for rendering HTML templates

GPIO.setwarnings(False)                  # Disable warnings related to GPIO pins
GPIO.setmode(GPIO.BCM)                   # Set the GPIO pin numbering mode to BCM
GPIO.cleanup()                           # Clean up the GPIO pin channels

instance = dht11.DHT11(pin=14)           # Create an instance of the DHT11 sensor using pin 14

app = Flask(__name__)                    # Create a new Flask application instance

@app.route('/')
def index():
    try:
        conn = sqlite3.connect('dht11.db') # This connects to a SQLite database file named dht11.db
        c = conn.cursor() # This creates a cursor object to interact with the database
        c.execute("SELECT * FROM readings ORDER BY datetime DESC LIMIT 10") # This executes a SQL SELECT statement to retrieve the last 10 rows from a table named readings, ordered by datetime in descending order
        rows = c.fetchall() # This fetches all the rows returned by the SELECT statement
        readings = [] # This creates an empty list to store the retrieved readings
        
        for row in rows: # This loops through each row returned by the SELECT statement
            readings.append({ 
                'datetime': row[1],
                'temperature': row[2],
                'humidity': row[3]
            })
        
        while True:
            result = instance.read() # This reads the temperature and humidity values from the sensor and stores them in a variable named result
            if result.is_valid():  # This checks if the sensor reading is valid
                temp = result.temperature # This extracts the temperature value from the sensor reading and stores it in a variable named temp
                hum = result.humidity # This extracts the humidity value from the sensor reading and stores it in a variable named hum
                dt = datetime.datetime.now() # This gets the current date and time and stores it in a variable named dt
                insertDHTDATA(dt, temp, hum) # This calls a function named insertDHTDATA and passes in the current datetime, temperature, and humidity values
                readings.insert(0, { # This inserts a dictionary containing the current datetime, temperature, and humidity values at the beginning of the readings list
                    'datetime': dt,
                    'temperature': temp,
                    'humidity': hum
                })
                return render_template('index.html', readings=readings) # This renders an HTML template named index.html and passes in the readings list as a variable named readings
            else:
                sleep(2) # Wait 2 seconds before retrying the sensor reading
                
    except sqlite3.Error as e: # This catches any SQLite errors that occur within the try block and stores them in a variable named e
        print(f'Could not retrieve data! {e}') # This prints an error message containing the SQLite error
        return 'Error retrieving data' # This returns an error message


def insertDHTDATA(dt, temp, hum):
    try:
        conn = sqlite3.connect('dht11.db')
        query ='INSERT INTO DHT11TABLE (DATETIME, TEMPERATURE, HUMIDITY)VALUES(?,?,?)'

        # Create a database/table
        c = conn.cursor()
        c.execute("CREATE TABLE IF NOT EXISTS readings (id integer PRIMARY KEY AUTOINCREMENT, datetime timestamp, temperature float, humidity float)")

        query = "INSERT INTO readings (DateTime,Temperature,Humidity) VALUES (?,?,?)"
        values = (dt, temp, hum)
        c.execute(query, values)
        conn.commit()
    except sqlite3.Error as e:
        conn.rollback()
        print(f'Could not insert ! {e}')
    finally:
        conn.close()

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)


