import firebase_admin
from firebase_admin import firestore
import flask
#-----------Signal processing code-----------
from functions import ReadFile, filteremg, filter_with_set_values, NotchFilter, BandPassFilter, Compute_RMS, LowPassButter, CreateThreshold, FindActivity, FindPedalStrokeStart
import matplotlib.pyplot as plt
import numpy as np
import math

from crud import upload_image_file

# -----------------------Python code for service----------------------
app = flask.Flask(__name__)

firebase_admin.initialize_app()
SUPERHEROES = firestore.client().collection('muscledata')

@app.route('/processdata', methods=['POST'])
def create_hero():
    req = flask.request.json
    hero = SUPERHEROES.document()
    hero.set(req)

    return flask.jsonify({'id': 'hallo Gunnar'}), 201

@app.route('/processdata/<id>')
def read_hero(id):
    return flask.jsonify(_ensure_hero(id).to_dict())

@app.route('/processdata/<id>', methods=['PUT'])
def update_hero(id):
    _ensure_hero(id)
    req = flask.request.json
    SUPERHEROES.document(id).set(req)
    return flask.jsonify({'success': True})

@app.route('/processdata/<id>', methods=['DELETE'])
def delete_hero(id):
    _ensure_hero(id)
    SUPERHEROES.document(id).delete()
    return flask.jsonify({'success': True})

def _ensure_hero(id):
    try:
        return SUPERHEROES.document(id).get()
    except:
        flask.abort(404)


# ---------------------Python code for signal processing-------------------------


#Fetching EMG file
data = ReadFile('OpenBCI-RAW-2018-11-07_14-47-55_biking_fixed_Reb.txt')
SamplFreq = 250


#Creating vectores
pin1 = []
pin2 = []
pin3 = []
pin4 = []
pin5 = []
pin6 = []
pin7 = []
pin8 = []
TimeStamp = []

Fs = 250

#Data inserting into their vectors
for emgf_tmp in data:
    pin1.append(emgf_tmp[' Pin1']) #Adding measures from pin 1 - Gastrocnemius Laterialis
    pin2.append(emgf_tmp[' Pin2']) #Adding measures from pin 2 - Gastrocnemius Medialis
    pin3.append(emgf_tmp[' Pin3']) #Adding measures from pin 3 - Tibialis Anterior
    pin4.append(emgf_tmp[' Pin4']) #Adding measures from pin 4 - Vastus Lateralis
    pin5.append(emgf_tmp[' Pin5']) #Adding measures from pin 5 - Bicep Hamstrings
    pin6.append(emgf_tmp[' Pin6']) #Adding measures from pin 6 - Rectur Femoris

#Change all values in the lists from string to number
pin1 = list(map(float, pin1))
pin2 = list(map(float, pin2))
pin3 = list(map(float, pin3))
pin4 = list(map(float, pin4))
pin5 = list(map(float, pin5))
pin6 = list(map(float, pin6))

#get time values
time = np.array([i/SamplFreq for i in range(0,len(pin3),1)])

# Putting muscles into one array
emgf_tmp = np.array([pin1, pin2, pin3, pin4, pin5, pin6], dtype = float)
# Transpose array to get XXXX x 6
#emgf_tmp_tmp = emgf_tmp.transpose()

emgf= emgf_tmp[:,(160*Fs)-1:]

# Extracting mean values to have every datapoint be placed at 0
emg=np.empty([emgf.shape[1], len(emgf)], dtype=float)

counter = -1
for row in emgf:
    counter += 1
    mean_value = np.mean(row)
    i = 0
    while i < len(row): #length of row is 14447
        emg[i][counter] = row[i] - mean_value
        i += 1

    
#Filter the stuff
emg_Notch = NotchFilter(250,emg)
emg_filtered = BandPassFilter(250,emg_Notch,20,124)

#Calculate the rms
emg_rms = Compute_RMS(emg_filtered,10)

#Low pass filter on the stuff
emg_rms_LP = LowPassButter(250,emg_rms,10)

#Create threshold
emg_thresh = CreateThreshold(emg_rms_LP)

#Calculate activity
emg_activity = FindActivity(emg_rms_LP, emg_thresh)

# Find start and end point of each period stroke
time_max = emg_rms_LP.shape[0]/Fs
time_vector = np.linspace(0, time_max , num=emg_rms_LP.shape[0])*10
x_start = FindPedalStrokeStart(emg_activity[:,0], time_vector)

#Create colors for graph
Litir = ['yellow', 'salmon','green','blue','orange','lime']

#Plot circles
s=0
while s < len(x_start)-1:
    #Create circles
    byrjun = int(x_start[s])
    print(byrjun)
    endir = int(x_start[s+1]-1)
    print(endir)


    cycle_length = endir-byrjun+1

    #Create a vector that starts at 0 and goes to the length of the b-e
    cycle_vect = np.arange(0,endir-byrjun+1)

    #Create a radian vector
    rad_vect = np.linspace(-math.pi/6,(2*math.pi)+(-math.pi/6),cycle_length)


    #Create a circle
    #x = radius*np.cos(rad_ang)
    #y = radius*np.sin(rad_ang)

    fig = plt.figure()
    # Create the baseline circles.
    circle1 = plt.Circle((0, 0), 2, color='k', fill=False)
    circle2 = plt.Circle((0, 0), 3, color='k', fill=False)
    circle3 = plt.Circle((0, 0), 4, color='k', fill=False)
    circle4 = plt.Circle((0, 0), 5, color='k', fill=False)
    circle5 = plt.Circle((0, 0), 6, color='k', fill=False)
    circle6 = plt.Circle((0, 0), 7, color='k', fill=False)
    circle7 = plt.Circle((0, 0), 8, color='k', fill=False)
    circle8 = plt.Circle((0, 0), 8, color='k', fill=False)


    ax = plt.gca()
    ax.cla() # clear things for fresh plot

    # change default range so that new circles will work
    ax.set_xlim((-10, 10))
    ax.set_ylim((-10, 10))
    # some data

    ax.add_artist(circle1)
    ax.add_artist(circle2)
    ax.add_artist(circle3)
    ax.add_artist(circle4)
    ax.add_artist(circle5)
    ax.add_artist(circle6)
    ax.add_artist(circle7)
    ax.add_artist(circle8)

    n = 0
    while n < emg_activity.shape[1]:
        j = 0
        new_active = emg_activity[byrjun:endir,n]
        inwhile = False
        i = 0

        while i < cycle_length:
            inWhile = False
            if i>j:
                j = i

            while j<len(new_active) and new_active[j]==1:
                if inWhile == False:
                    fyrst = j       #find the first activity in the cycle
                    inWhile = True
                sidast = j
                j = j+1

            if inWhile == True:
                r_angl = -rad_vect[fyrst:sidast]
                radius = n+2.5
                x = radius*np.cos(r_angl)
                y = radius*np.sin(r_angl)
                plt.plot(x,y,'r',linewidth = 13,color = Litir[n])
            i += 1
        n +=1

    #Do some plotting
    #muscle1 = plt.plot(x,y,'r',linewidth = 13)
    plt.show()
    s +=1

    # Save images
    image_url = upload_image_file(request.files.get('image'))

    




if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
