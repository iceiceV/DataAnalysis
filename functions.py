import csv
import numpy as np
import scipy as sp
from scipy import signal
import matplotlib.pyplot as plt


def ReadFile(filename):
	try:
		#Start opening the file and read from it
		EMGFile = open(filename,'r')

		#reading all the lines
		lines = EMGFile.readlines()

		#close file
		EMGFile.close()

		#fixing EMG file
		FixEMGFile(filename,lines)

		#Opening the file again
		EMGFile2 = open(filename,'r')

		#Reading in data and making the program deviding the words with ","
		reader = csv.DictReader(EMGFile2, delimiter = ',')
		
		#create an empty array
		data = []

		#Reading all lines and save
		for row in reader:
			data.append(row)

		#Close file
		EMGFile2.close()

		#Returning data to user
		return data

		#If the file is not found, alerting the user
	except FileNotFoundError as err:
		print("Can not open file")
		exit()





#Function that fixes the EMG file by deleting the first lines that are not data
def FixEMGFile(filename,lines):
	#Changing the file ef % is the first letter in the file
	if lines[0][0] == '%':

		#Opening the file to write into it
		EMGFile = open(filename,'w')

		#Writing the previous file into the new one wihtout the first lines
		linecounter = 0
		for line in lines:
			if linecounter < 6:
				linecounter = linecounter + 1
				if linecounter == 6:
					EMGFile.write("SampleIndex, Pin1, Pin2, Pin3, Pin4, Pin5, Pin6, Pin7, Pin8, acc1, acc2, acc3, TimeStamp\n")
			else:
				EMGFile.write(line)
			
		#Close file
		EMGFile.close()



#Function that remove mean in the EMG signal
def CorrectMean(EMGData):
	emg_correctmean = EMGData - np.mean(EMGData)
	#Returning corrected mean to user
	return emg_correctmean



#Filtering EMG, code taken from this website: https://scientificallysound.org/2016/08/22/python-analysing-emg-signals-part-4/
def filteremg(time, emg, low_pass=-1000, sfreq=1000, high_band=-1050, low_band=450):
    """
    time: Time data
    emg: EMG data
    high: high-pass cut off frequency
    low: low-pass cut off frequency
    sfreq: sampling frequency
    """
    
    # normalise cut-off frequencies to sampling frequency
    high_band = high_band/(sfreq/2)
    low_band = low_band/(sfreq/2)
    
    # create bandpass filter for EMG
    b1, a1 = signal.butter(4, [high_band,low_band], btype='bandpass')
   
    
    # process EMG signal: filter EMG
    emg_filtered = signal.filtfilt(b1, a1, emg)    
    
    # process EMG signal: rectify
    emg_rectified = abs(emg_filtered)
    
    # create lowpass filter and apply to rectified signal to get EMG envelope
    low_pass = low_pass/sfreq
    b2, a2 = signal.butter(4, low_pass, btype='lowpass')
    emg_envelope = signal.filtfilt(b2, a2, emg_rectified)
    
    # plot graphs
    fig = plt.figure()
    plt.subplot(1, 2, 1)
    plt.subplot(1, 2, 1).set_title('Unfiltered,' + '\n' + 'unrectified EMG')
    plt.plot(time, emg)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    
    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title('Filtered,' + '\n' + 'rectified EMG: ' + str(int(high_band*sfreq)) + '-' + str(int(low_band*sfreq)) + 'Hz')
    plt.plot(time, emg_rectified)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.plot([0.9, 1.0], [1.0, 1.0], 'r-', lw=5)
    plt.xlabel('Time (sec)')

    # plt.subplot(1, 4, 3)
    # plt.subplot(1, 4, 3).set_title('Filtered, rectified ' + '\n' + 'EMG envelope: ' + str(int(low_pass*sfreq)) + ' Hz')
    # plt.plot(time, emg_envelope)
    # plt.locator_params(axis='x', nbins=4)
    # plt.locator_params(axis='y', nbins=4)
    # plt.ylim(-1.5, 1.5)
    # plt.plot([0.9, 1.0], [1.0, 1.0], 'r-', lw=5)
    # plt.xlabel('Time (sec)')
    
    # plt.subplot(1, 4, 4)
    # plt.subplot(1, 4, 4).set_title('Focussed region')
    # plt.plot(time[int(0.9*1000):int(1.0*1000)], emg_envelope[int(0.9*1000):int(1.0*1000)])
    # plt.locator_params(axis='x', nbins=4)
    # plt.locator_params(axis='y', nbins=4)
    # plt.xlim(0.9, 1.0)
    # plt.ylim(-1.5, 1.5)
    # plt.xlabel('Time (sec)')

    plt.show()

    # fig_name = 'fig_' + str(int(low_pass*sfreq)) + '.png'
    # fig.set_size_inches(w=11,h=7)
    # fig.savefig(fig_name)



# Filtering EMG signal with using methods from this website (part 3): https://scientificallysound.org/2016/08/18/python-analysing-emg-signals-part-3/
def filter_with_set_values(time,emg):
# time: time data
# emg: corrected mean emg data

    #create bandpass filter for EMG
    high = 5 #20/(1000/2)
    low = 50 #450/(1000/2)
    b, a = sp.signal.butter(4,[high, low], btype = 'bandpass')

    # process EMG signal: filter EMG
    emg_filtered = sp.signal.filtfilt(b,a,emg)
  
    # plot comparison of unfiltered vs filtered mean-corrected EMG
    fig = plt.figure()
    plt.subplot(1,2,1)
    plt.subplot(1, 2, 1).set_title('Unfiltered EMG')
    plt.plot(time, emg)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')

    plt.subplot(1, 2, 2)
    plt.subplot(1, 2, 2).set_title('Filtered EMG')
    plt.plot(time, emg_filtered)
    plt.locator_params(axis='x', nbins=4)
    plt.locator_params(axis='y', nbins=4)
    #plt.ylim(-1.5, 1.5)
    plt.xlabel('Time (sec)')
    plt.ylabel('EMG (a.u.)')
    plt.show()


def NotchFilter(fs,InputSignal):
    f0 = 50.0   #freqyency to be removed from signal (Hz)
    Q = 30.0    #Quality factor, Q = w0/bw,
    w0 = f0/(fs/2)  #normalized frequency
    #Design the notch filter
    b, a = sp.signal.iirnotch(w0,Q)
    #numerator b and denominator a that are polynomials of the IIR filter
    
    #go through all muscles and filter them
    i = 0
    yf = np.empty([InputSignal.shape[0], InputSignal.shape[1]], dtype=float)
    
    while i < InputSignal.shape[1]:
        yf[:,i] = sp.signal.lfilter(b,a,InputSignal[:,i])
        i+=1
    return yf

def BandPassFilter(fs,InputSignal,LP,HP):
    nyq = 0.5 * fs      #calculate nyquist frequency
    low = LP / nyq
    high = HP / nyq
    order = 5           #assume we are using 5th order butter banpass filter
    b, a = sp.signal.butter(order, [low, high], btype='band')
    #numerator b and demoninator a that are polynomials of the filter
    i = 0
    yf = np.empty([InputSignal.shape[0], InputSignal.shape[1]], dtype=float)
    
    while i < InputSignal.shape[1]:
        yf[:,i] = sp.signal.lfilter(b,a,InputSignal[:,i])
        i +=1
    return yf

def Compute_RMS(Signal,Interval):
    #Calculate the RMS of a given signal
    n = 0
    rms_values = np.empty([Signal.shape[0]//10, Signal.shape[1]], dtype=float)
    vect = np.arange(0,Signal.shape[0]-1-Interval, Interval)

    while n < Signal.shape[1]:
        counter = 1
        #rms_values = [0]*len(vect)  #Initialize an array
        for i in vect:
            if i == 0:
                rms_values[0,n] = RMS(Signal[i:Interval,n])
            else:
                rms_values[counter,n] = RMS(Signal[i+1:i+Interval,n])
                counter += 1
        n +=1
    return rms_values 


def RMS(Signal):
    rms_val = np.sqrt(np.mean(Signal**2))
    return rms_val

def LowPassButter(fs,Signal,LP):
    nyq = 0.5 * fs
    w0 = LP/nyq
    order = 3
    b,a = sp.signal.butter(order, w0, btype = 'low')
    #numerator b and demoniator a that are polynomials of the filter
    yf = np.empty([Signal.shape[0], Signal.shape[1]], dtype=float)
    i = 0
    while i < Signal.shape[1]:
        yf[:,i] = sp.signal.lfilter(b,a,Signal[:,i])
        i +=1
    return yf

def CreateThreshold(Signal):
    thresh = np.empty([Signal.shape[0], Signal.shape[1]], dtype=float)
    thresh[0,:] = Signal[0,:]

    n = 0
    while n < Signal.shape[1]:
        count = 1
        while count <Signal.shape[0]:
            if count < 50:
                thresh[count,n] = (15*Signal[count,n] + 85*thresh[count-1,n])/100
            else:
                thresh[count,n] = (1*Signal[count,n] + 99*thresh[count-1,n])/100
            count +=1
        n +=1
    return thresh

def FindActivity(Signal,thresh):
    active = np.empty([Signal.shape[0], Signal.shape[1]], dtype=float)
    n = 0

    while n< Signal.shape[1]:
        i = 0
        while i < Signal.shape[0]:
            if Signal[i,n]>=thresh[i,n]:
                active[i,n] = 1
            else:
                active[i,n] = 0
            i += 1
        n += 1
    return active

def circr(radius,rad_ang):
    x = radius*cos(rad_ang)
    y = radius*sin(rad_ang)
    return

def FindPedalStrokeStart(Signal, time):
# Find start point of first pedal stroke for one muscle
    #x_coord = []
    x_coord = np.empty(0, dtype=int)
    x_start = []
    i = 0
    s = 0
    while i < Signal.shape[0]-1:
        if Signal[i] == 0 and Signal[i+1] == 1:
            x_coord = np.append(x_coord,i+1)
        i += 1
    while s < len(x_coord):
        if time[x_coord[s]] > 10:
            x_start = np.append(x_start,x_coord[s])
        s += 1
    return x_start













