import time
import csv
import ltr559
from bme280 import BME280
from enviroplus import gas
from pms5003 import PMS5003

pms5003 = PMS5003()

try:
    from smbus2 import SMBus
except ImportError:
    from smbus import SMBus

import logging

import datetime

logging.basicConfig(
    format='%(asctime)s.%(msecs)03d %(levelname)-8s %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""weather.py - Print readings from the BME280 weather sensor.

Press Ctrl+C to exit!

""")

bus = SMBus(1)
bme280 = BME280(i2c_dev=bus)

name_datafile = 'data_' + str(datetime.datetime.now()) + '.txt'

datafile = open(name_datafile, "w")

field_names = ['Data;', 'Temperatura (°C);', 'Pressione (hPa);', 'Umidità (%);','Intensità Luminosa(Lm)''Prossimità','Gas','Particolato(ug)']
datafile.writelines(field_names)

while True:
    x = datetime.datetime.now()
    temperature = bme280.get_temperature()
    pressure = bme280.get_pressure()
    humidity = bme280.get_humidity()
    lux = ltr559.get_lux()
    proximity = ltr559.get_proximity()
    gasensor = gas.read_all()
    particulate = pms5003.read()

    logging.info("""\n Temperature: {:05.2f} *C \n Pressure: {:05.2f} hPa \n Relative humidity: {:05.2f} % \n Lux: {:05.2f}Lm \n Particulate: {:05.2f} ug """.format(temperature, pressure, humidity,lux, particulate))
    datafile.write('\n')
    datafile.write(str(x)+';'+str(temperature)+';'+str(pressure)+';'+str(humidity)+';'+str(lux)+';'+str(particulate)+';'+str(proximity)+';'+str(gasensor))
    datafile.close()
    time.sleep(900) #valore in secondi, 1800 per registrare i dati ogni 30 minuti
    datafile = open(name_datafile, "a")
