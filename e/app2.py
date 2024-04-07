from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model
import time
import threading 
import textToSpeechModule

# THE IDEA:: SCAN A COLUMN. WHEN A CAN IS DETECTED, WE STOP THE COLUMN AND GATHER THE X 

app = Flask(__name__)

global playable
playable = True  # Initialize playable as True

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()






# Initialize serial connection (update port and baudrate as per your Arduino setup)

def classify_image(image):
    # Resize the raw image into (224-height,224-width) pixels
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)

    image.imshow();
    cv2.waitkey();

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

def joke_thread():
    time.sleep(5)  
    while True:
        global playable
        playable = True
        if confidence_score > 0.8 and playable:
            playable = False
            textToSpeechModule.makeJoke()
            print("works")
            time.sleep(15)  # Cooldown period

def gen_frames():
    global playable, confidence_score  # Declare global variables
    camera = cv2.VideoCapture(0)
    threading.Thread(target=joke_thread).start()  # Start the joke_thread
    while True:
        # Grab the webcamera's image
        ret, frame = camera.read()
        if not ret:
            break

        
        class_name, confidence_score = classify_image(frame)

        # Draw bounding box if confidence score is high
        if confidence_score > 0.8:
            # Assuming bounding box coordinates (x, y, w, h) are returned by classify_image
            bounding_box = (0, 0, 50, 50)  # Replace with actual bounding box coordinates
            x, y, w, h = bounding_box
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(frame, class_name, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

        # Draw prediction text on the frame
        cv2.putText(frame, f'Class: {class_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
        cv2.putText(frame, f'Confidence: {confidence_score:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

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

if __name__ == "__main__":
    app.run(debug=True)
