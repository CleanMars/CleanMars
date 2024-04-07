import cv2
import numpy as np
from keras.models import load_model
import time 
import serial
import textToSpeechModule as tts

# 477 by 620


# Load the model
model = load_model("keras_model.h5", compile=False)

# Load the labels
class_names = open("labels.txt", "r").readlines()

def loopsize_image(frameCopy):
    for i in range(0, 590, 40):
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
        print (name)
        if(confidence_score_cropped > 0.82 and name == "2 can\n"):
            print(i + 75)
            print("MIDDLE")
            cv2.destroyAllWindows()
            return i + 75 #middle!!!

        cv2.waitKey(1)  # Add a small delay for display (10 milliseconds)



        # Exit the loop if a key is pressed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break



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
    camera = cv2.VideoCapture(2)
    while True:
        ret, frame = camera.read()
        frameCopy = frame
        if not ret:
            break
        cv2.imshow('Camera', frame)     #display


        class_name, confidence_score = classify_image(frame)

        print(class_name)
        print(confidence_score)
        if(confidence_score > 0.82 and "0 base\n" != class_name):
            print("success")
            xPos = loopsize_image(frameCopy)
            #send signal (xPos)


        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    camera.release()
    cv2.destroyAllWindows()

#def joke_thread():
 #   time.sleep(5)  
  #  while True:
   #     global playable
    #    playable = True
     #   if confidence_score > 0.82 and playable:
      #      playable = False
       #     tts.makeJoke()
        #    print("works")
         #   time.sleep(15)  # Cooldown period


if __name__ == "__main__":
    gen_frames()