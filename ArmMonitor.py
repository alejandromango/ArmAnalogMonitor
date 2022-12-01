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
arm = io.TextIOWrapper(io.BufferedReader(ser), newline='\n')

monitor = numpy.array([])
angleTimes = numpy.array([])
angles = numpy.array([])

def endExperiment(data, times, log):
    angleData = pandas.DataFrame({'Time': times, 'Angle': data})
    angleData.to_csv("AnalogAngleData.csv")
    print(monitor.shape)
    logData = pandas.DataFrame(monitor)
    logData.to_csv("AnalogLogData.csv")
while (True):
    time.sleep(0.001)
    while (True):
        a=arm.readline()
        if (a == ""):
            break
        else:
            aTerms = a.split(";")
            if (int(aTerms[1]) == 1):
                print(aTerms[2])
                monitor = numpy.append(monitor, aTerms)
                if ("Finished all movement cycles" in aTerms[2]) | ("Aborted Run" in aTerms[2]):
                    endExperiment(angles, angleTimes, monitor)
                    quit()
            elif (int(aTerms[1]) == 0):
                angleTimes = numpy.append(angleTimes, float(aTerms[0]))
                angles = numpy.append(angles, float(aTerms[2]))
                # if len(angles) > 5000:#("Finished all movement cycles" in aTerms[2]) | ("Aborted Run" in aTerms[2]):
                #     endExperiment(angles, angleTimes, monitor)
                #     quit()
