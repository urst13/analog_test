# Konfigurationsvariablen

# Maximaler Druck in bar, der dem 5V Eingangsspannungsbereich entspricht
max_druck = 250




# Kontinuierliches Auslesen des A0-Eingangs, print in Konsole

import board
import time
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import csv
 
# Initialize the I2C interface
i2c = busio.I2C(board.SCL, board.SDA)
 
# Create an ADS1115 object
ads = ADS.ADS1115(i2c)
 
# Define the analog input channel
channel = AnalogIn(ads, ADS.P0)

# Schwellwert für den Start der Messung
start_schwellwert = 40

# Schwellwert für das Beenden der Messung
stop_schwellwert = 30

# Dauer (in Sekunden), die der Schwellwert unterschritten sein muss, um die Messung zu beenden
stop_dauer = 30

# Zähler für die Messungen
messung_nummer = 1

# CSV-Dateiname und Header
csv_dateiname = "messungen.csv"
csv_header = ["Messung", "Zeitpunkt", "Gemessene Spannung (V)", "Druck (bar)"]

# Funktion zum Schreiben der Messwerte in die CSV-Datei
def schreibe_in_csv(messung, zeitpunkt, gemessene_spannung, druck):
    with open(csv_dateiname, mode="a", newline="") as file:
        writer = csv.writer(file)
        if file.tell() == 0:
            writer.writerow(csv_header)
        writer.writerow([messung, zeitpunkt, gemessene_spannung, druck])

# Loop für die Messungen
messung_gestartet = False
messung_startzeit = 0

while True:
    gemessene_spannung = channel.voltage
    druck = (gemessene_spannung / 5.0) * max_druck
    zeitpunkt = time.strftime("%Y-%m-%d %H:%M:%S")

    if not messung_gestartet and druck > start_schwellwert:
        print("Messung gestartet")
        messung_gestartet = True
        messung_startzeit = time.time()

    if messung_gestartet:
        schreibe_in_csv(messung_nummer, zeitpunkt, gemessene_spannung, druck)

        if druck < stop_schwellwert:
            if time.time() - messung_startzeit >= stop_dauer:
                print("Messung beendet")
                messung_gestartet = False
                messung_nummer += 1

    time.sleep(0.5)