#!/usr/bin/env python3
import re
import sys

class ds1820:
    sensor_path = None
    def __init__(self, sensor = None):

        if sensor is None:
            with open("ds1820_path", "r") as fd:
                sensor = fd.readline().strip()

        self.sensor_path = sensor

    def read(self):
        value = 0

        try:
            with open(self.sensor_path, "r") as f:
                line = f.readline()

                if re.match(r".*:\s+crc=[0-9a-f]{2}\s+YES", line):

                    line = f.readline()
                    m = re.match(r"(.{2}\s+){9}t=([+-]?\d+)", line)

                    if m:
                        value = float(m.group(2)) / 1000.0
                    else:
                        print("No match on second line")
                else:
                    print("CRC not valid")

        except IOError as err:
            print ("Error reading", self.sensor_path, ": IOError\n", err)

        return float(value)


if __name__=='__main__':
    import time

    # sens = "/sys/bus/w1/devices/28-031771c50bff/w1_slave"
    sens = None

    if len(sys.argv) == 2:
        sens = sys.argv[1]

    tempsen = ds1820(sens)

    print("Reading Sensor for 2 minutes...")

    for i in range(0,120):
        print(round(tempsen.read(), 2), "°C")
        time.sleep(0.5)
