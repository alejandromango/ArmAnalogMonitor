import serial
import argparse
import io
import numpy
import pandas
import time

parser = argparse.ArgumentParser(description='This script monitors the serial output of the ArmAnalog firmware.\
                                              The associated firmware is found at \
                                              https://github.com/alejandromango/BME207_SJSU_ArmAnalogController')
parser.add_argument('port', type=str, help='serial port to be monitored')
args = parser.parse_args()
print("Opening port at ", args.port)
ser = serial.Serial(args.port, 115200)  # open serial at the port given in the arguments
arm = io.TextIOWrapper(io.BufferedReader(ser))

armMonitor = []
angleMonitor = []
while (True):
    time.sleep(0.001)
    while (True):
        a=arm.readline()
        if (a == ""):
            break
        else:
            aTerms = a.split(";")
            if (int(aTerms[1]) == 1):
                print(aTerms)
                # armMonitor.append(a)
                if ("Finished all movement cycles" in aTerms[2]) | ("Aborted Run" in aTerms[2]):
                    # endExperiment(angleMonitor, armMonitor)
                    quit()

# def endExperiment(data, log):

