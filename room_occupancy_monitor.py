#app.py
#Jazmin GK 04/02/2025 
from flask import Flask, render_template, request
from gpiozero import LED
from time import time

app = Flask(__name__)

red_led = LED(4)
green_led = LED(21)

@app.route('/')
def index(enviro_message: str = 'none'):
    return render_template('index.html', message_text=enviro_message)

@app.route('/automate', methods=['POST'])
def control():
    global start_time, end_time
    task = request.form['task']

    if task == 'Occupied':
        red_led.on()
        green_led.off()
        start_time = time()
        return index("Occupied: Timer started.")

    elif task == 'Open':
        red_led.off()
        green_led.on()
        end_time = time()
        return index("Open: Timer stopped.")

    elif task == 'Duration':
        #start_time = request.form.get('start_time', type=float)
        #end_time = request.form.get('end_time', type=float)
        
        if start_time is None or end_time is None:
            return index("Error: Please click Occupied and Open before checking the duration.")
        
        exam_seconds = end_time - start_time
        hours = int(exam_seconds // 3600)
        minutes = int((exam_seconds % 3600) // 60)
        seconds = int(exam_seconds % 60)

        return index("Duration: {:d}h {:d}m {:d}s".format(hours, minutes, seconds))
    
    return index("Invalid Action: {:s} is not recognized.".format(task))


