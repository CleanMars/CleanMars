import serial
import time

print("Starting moveController.py...")

# Establish serial connection (adjust port and baud rate as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# motorSerial = serial.Serial('/dev/ttyUSB1', 9600, timeout=1) #FOR AKIKO


def test():
    try:
        while True:
            # write distances to arduino from CLI

                deg = input('Enter distance from Sensor 1: ')
                print(deg)
                ser.write(deg.encode())
    except KeyboardInterrupt:
        print('Program terminated by user')

    finally:
        # Close serial connection
        ser.close()

if __name__ == "__main__":
     test()
     
