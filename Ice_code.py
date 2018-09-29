from functions import ReadFile
import matplotlib.pyplot as plt

#Sæki gögnin úr EMG skrá
data = ReadFile('OpenBCI-RAW-2018-09-26_18-11-18.txt')

#bý til tóma vektora
pin1 = []
pin2 = []
pin3 = []
pin4 = []
pin5 = []
pin6 = []
pin7 = []
pin8 = []

#hleð gögnum inn í viðeigandi vektora
for x in data:
	pin1.append(x[' Pin1']) #Bæti við mælingum frá pinna 1
	pin2.append(x[' Pin2']) #Bæti við mælingum frá pinna 2
	pin3.append(x[' Pin3']) #Bæti við mælingum frá pinna 3
	pin4.append(x[' Pin4']) #Bæti við mælingum frá pinna 4
	pin5.append(x[' Pin5']) #Bæti við mælingum frá pinna 5
	pin6.append(x[' Pin6']) #Bæti við mælingum frá pinna 6
	pin7.append(x[' Pin7']) #Bæti við mælingum frá pinna 7
	pin8.append(x[' Pin8']) #Bæti við mælingum frá pinna 8


#Change all values in the lists from string to number
pin1 = list(map(float, pin1))
pin2 = list(map(float, pin2))
pin3 = list(map(float, pin3))
pin4 = list(map(float, pin4))
pin5 = list(map(float, pin5))
pin6 = list(map(float, pin6))
pin7 = list(map(float, pin7))
pin8 = list(map(float, pin8))

#plt.plot(pin1[90000:],'b')
plt.plot(pin4[90000:],'r')
plt.show()
