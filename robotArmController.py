import serial
import time

# Establish serial connection (adjust port and baud rate as needed)
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

def send_position(position):
    # Send the position as a string over serial
    ser.write(str(position).encode())

def handleArmMovement():
    try:
        while True:
            # Write position to Arduino from CLI
            pos = int(input('Enter servo position (0-180 degrees): '))
            send_position(pos)
    
    except KeyboardInterrupt:
        print('Program terminated by user')

    finally:
        # Close serial connection
        ser.close()
