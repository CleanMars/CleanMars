import cv2
import numpy as np
from keras.models import load_model
import time 
import textToSpeechModule as tts
import threading

# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = [name.strip() for name in open("labels.txt", "r")]

confidence_score = 0.0

def loopsize_image(frameCopy):
    for i in range(0, 590, 20):
        # Clear the frame on each iteration
        frame = frameCopy.copy()

        # Calculate the coordinates for the rectangle
        top_left = (i, 0)
        bottom_right = (i + 150, 620)

        # Draw the rectangle on the frame
        color = (255, 255, 255)  # White color
        thickness = 2
        cv2.rectangle(frame, top_left, bottom_right, color, thickness)
        
        # Display the frame
        cv2.imshow("framecopy", frame)

        cropped = frame[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]]

        cv2.imshow("fully cropped", cropped)

        name, confidence_score_cropped = classify_image(cropped)
        print(confidence_score_cropped)
        print(name)
        if confidence_score_cropped > 0.82:
            print(i + 75)
            return i + 75  # middle!!!

     # Add a small delay for display (10 milliseconds)

def classify_image(image):
    image = cv2.resize(image, (224, 224), interpolation=cv2.INTER_AREA)
    image = np.asarray(image, dtype=np.float32).reshape(1, 224, 224, 3)
    # Normalize the image array
    image = (image / 127.5) - 1
    # Predict the model
    prediction = model.predict(image)
    index = np.argmax(prediction)
    class_name = class_names[index]
    confidence_score = prediction[0][index]
    return class_name, confidence_score

def gen_frames():
    camera = cv2.VideoCapture(0)
    while True:
        ret, frame = camera.read()
        frameCopy = frame.copy()
        if not ret:
            break
        cv2.imshow('Camera', frame)     # Display the camera feed

        class_name, confidence_score = classify_image(frame)

        print(class_name)
        print(confidence_score)
        if confidence_score > 0.82 and class_name == "0 can":
            print("success")
            xPos = loopsize_image(frameCopy)
            # Send signal (xPos)
            time.sleep(3)

        key = cv2.waitKey(1)
        if key == ord('q'):
            break

    # Release the camera and close OpenCV windows
    camera.release()
    cv2.destroyAllWindows()

def joke_thread():
    time.sleep(5)  
    while True:
        time.sleep(1)
        global confidence_score
        if confidence_score > 0.82:
            tts.makeJoke()
            print("works")
            time.sleep(15)  # Cooldown period

if __name__ == "__main__":
    #joke_thread = threading.Thread(target=joke_thread)
    #joke_thread.start()

    gen_frames()
