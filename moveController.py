import serial
import time

print("Starting moveController.py...")

# Establish serial connection (adjust port and baud rate as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
# motorSerial = serial.Serial('/dev/ttyUSB1', 9600, timeout=1) #FOR AKIKO

def read_distance():
    # Read response from Arduino
    response1 = ser.readline().decode().strip()
    response2 = ser.readline().decode().strip()

    # Parse response and extract distance values
    if response1.startswith('Distance') and response2.startswith('Distance'):
        distance1 = int(response1.split(':')[-1].strip())
        distance2 = int(response2.split(':')[-1].strip())
        return distance1, distance2
    else:
        return None, None

# FOR AKIKO{
#def rotateRight():

#def rotateLeft():

#def moveForward():

#def moveBackward():
# }

def mainMovementLoop():
    try:
        while True:
            # Read distances from Arduino
            distance1, distance2 = read_distance()

            if distance1 is not None and distance2 is not None:
                print(f'Distance from Sensor 1: {distance1} cm')
                print(f'Distance from Sensor 2: {distance2} cm')

                # ser.write(bytearray(distance1))
                # ser.write(bytearray(distance2))

                #FOR AKIKO{
                #if({distance1} < 20):
                    #rotateRight()
                #if({distance2} < 20):
                    #rotateLeft()
                #if({distance1} < 20 and {distance2} < 20):
                    #moveBackward()
                    #moveRight()
                # }
            else:
                print('Failed to read distances from Arduino')
                # Delay for 1 second

    except KeyboardInterrupt:
        print('Program terminated by user')

    finally:
        # Close serial connection
        ser.close()
