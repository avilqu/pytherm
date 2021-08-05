#!/usr/bin/python3

''' Class for reading output of a DS18B20 temperature sensor from a Raspberry Pi.
    @author: Adrien Vilquin Barrajon <avilqu@gmail.com>
'''

import time


class DS18B20:
    ''' Contains output data from a DS18B20 temp sensor '''

    def __init__(self, sensor_dir):
        self.sensor_dir = sensor_dir
        self.sensor_id = sensor_dir[23:]
        self.w1_slave = sensor_dir + '/w1_slave'

    def read_raw(self):
        f = open(self.w1_slave, 'r')
        lines = f.readlines()
        f.close()
        return lines

    def read_temp(self):
        data = self.read_raw()
        while data[0].strip()[-3:] != 'YES':
            data = self.read_raw()

        temp_position = data[1].find('t=')
        if temp_position != -1:
            temp_string = data[1][temp_position+2:]
            temp_c = float(temp_string) / 1000.0
            return temp_c

    def print_temp(self):
        temp_c = self.read_temp()
        print(temp_c)

    def print_loop(self):
        while True:
            temp_c = round(self.read_temp(), 1)
            print(temp_c)
            time.sleep(1)
