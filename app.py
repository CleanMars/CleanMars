from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model
import serial
from textToSpeechModule import makeJoke

app = Flask(__name__)

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

# Initialize serial connection (update port and baudrate as per your Arduino setup)
ser = serial.Serial('/dev/ttyUSB0', 9600) # Adjust port accordingly

def classify_image(image):
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    # Make the image a numpy array and reshape it to the model's input shape.
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)

    # Normalize the image array
    image = (image / 127.5) - 1

    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]

    return class_name, confidence_score

def send_command_to_arduino():
    # Send command to Arduino (e.g., 'd' for detect)
    ser.write(bytearray(1))

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        # Grab the webcamera's image
        ret, frame = camera.read()
        if not ret:
            break

        class_name, confidence_score = classify_image(frame)

        # Draw prediction text on the frame
        cv2.putText(frame, f'Class: {class_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Confidence: {confidence_score:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        # If object detected and classified with high confidence
        if confidence_score > 0.8:
            # Send command to Arduino to move in front of the object
            # send_command_to_arduino()
            makeJoke()

        ret, buffer = cv2.imencode('.jpg', frame)
        frame = buffer.tobytes()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

def runModel():
    app.run(debug=True)
