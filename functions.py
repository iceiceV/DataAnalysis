import csv

def ReadFile(filename):
	try:
		#Byrja á að opna skránna og les allt úr henni
		EMGFile = open(filename,'r')

		#les inn allar línur
		lines = EMGFile.readlines()

		#Loka filenum
		EMGFile.close()

		#Laga EMG skjalið
		FixEMGFile(filename,lines)

		#Ona skránna aftur
		EMGFile2 = open(filename,'r')

		#les inn gögnin og læt forritið skipta á milli orða þegar það er ,
		reader = csv.DictReader(EMGFile2, delimiter = ',')
		
		#create an empty arrey
		data = []

		#les inn allar línur og vista
		for row in reader:
			data.append(row)

		#Loka filenum sem ég opnaði í byrjun
		EMGFile2.close()

		#skila til notandans gögnunum
		return data

		#ef að skjalið finnst ekki þá læt ég notanda vita
	except FileNotFoundError as err:
		print("Get ekki opnað skrá")
		exit()





#Fall sem að laga EMG file-inn með því að eyða fyrstu línunum sem ekki eru gögn
def FixEMGFile(filename,lines):
	#Breyti skjalinu ef % er fyrsti stafur í skjalinu
	if lines[0][0] == '%':

		#Opna skjalið til þess að skrifa í það
		EMGFile = open(filename,'w')

		#Skrifa gamlið skjalið aftur í nyja skjalið en sleppi fyrstu línunum
		linecounter = 0
		for line in lines:
			if linecounter < 6:
				linecounter = linecounter + 1
				if linecounter == 6:
					EMGFile.write("SampleIndex, Pin1, Pin2, Pin3, Pin4, Pin5, Pin6, Pin7, Pin8, acc1, acc2, acc3, TimeStamp\n")
			else:
				EMGFile.write(line)
			
		#Loka skjalinu
		EMGFile.close()
