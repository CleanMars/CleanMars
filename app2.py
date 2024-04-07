from flask import Flask, render_template, Response
import cv2
import numpy as np
from keras.models import load_model
import time
import threading 

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
            makeJoke()
            print("works")
            time.sleep(15)  # Cooldown period

def draw_bounding_box(frame, class_name, confidence_score):
    # Draw bounding box
    h, w, _ = frame.shape
    color = (0, 255, 0)  # Green color for bounding box
    cv2.rectangle(frame, (0, 0), (w, h), color, 2)
    # Add class name and confidence score
    cv2.putText(frame, f'Class: {class_name}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    cv2.putText(frame, f'Confidence: {confidence_score:.2f}', (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)
    return frame

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

        # Draw bounding box on the frame
        frame_with_box = draw_bounding_box(frame.copy(), class_name, confidence_score)

        # Encode the frame
        ret, buffer = cv2.imencode('.jpg', frame_with_box)
        frame_with_box = buffer.tobytes()

        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame_with_box + b'\r\n')

    camera.release()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(debug=True)
