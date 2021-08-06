#!/usr/bin/python3

''' Starting script for all pyterm functionalities.
    @author: Adrien Vilquin Barrajon <avilqu@gmail.com>
'''

import os
import glob
from datetime import datetime
import time

base_dir = '/sys/bus/w1/devices/'
data_dir = '/home/pi/pytherm/'


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
            return round(temp_c, 1)


def record_sensors(interval):
    if not os.path.exists(data_dir):
        os.mkdir(data_dir)

    start_date = datetime.now().strftime('%Y-%m-%d')
    data_filename = data_dir + start_date + '.txt'

    if os.path.exists(data_filename):
        f = open(data_filename, 'a')
    else:
        f = open(data_filename, 'w')

    while start_date == datetime.now().strftime('%Y-%m-%d'):
        data_string = datetime.now().strftime('%Y-%m-%dT%H:%M:%S') + ','
        for sensor in sensors:
            data_string = data_string + str(sensor.read_temp()) + ','
        data_string = data_string + '\n'
        f.write(data_string)
        time.sleep(interval)

    f.close()


sensors_dirs = glob.glob(base_dir + '28*')
sensors = []
for item in sensors_dirs:
    sensors.append(DS18B20(item))

if __name__ == "__main__":

    import argparse

    parser = argparse.ArgumentParser(
        description='Reads output from DS18B20 temperature sensors.')
    parser.add_argument(
        '-l', '--loop', help='print temp loop (1s interval)', action='store_true')
    parser.add_argument(
        '-r', '--record', help='record data to file with specified interval (in seconds)', type=int, dest='record')

    args = parser.parse_args()

    if args.loop and args.record:
        print('Loop and record functions are exclusive to each other.')
    elif args.loop:
        while True:
            for sensor in sensors:
                print(sensor.sensor_id, ':', sensor.read_temp())
            time.sleep(1)
    elif args.record:
        record_sensors(args.record)
    else:
        for sensor in sensors:
            print(sensor.sensor_id, ':', sensor.read_temp())
