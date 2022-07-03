import cv2
import requests


def get_image_webcam():

    face_csc = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
    cap = cv2.VideoCapture(0)

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()

        faces = face_csc.detectMultiScale(frame, 1.1, 4)
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 0, 0), 5)

        font = cv2.FONT_HERSHEY_PLAIN
        cv2.putText(frame,  
            'Presiona "s" para capturar la foto',  
            (50, 50),  
            font, 1,  
            (0, 255, 255),  
            1,  
            cv2.LINE_8)

        # Display the resulting frame
        cv2.imshow('Captura de rostro', frame)
        cv2.setWindowProperty('Captura de rostro', cv2.WND_PROP_TOPMOST, 1)
        if cv2.waitKey(1) & 0xFF == ord('s'):
            cv2.imwrite('image.jpg', frame)
            cap.release()
            cv2.destroyAllWindows()
            return "Success"

        if cv2.waitKey(1) & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            return "Failed"


def compare_images():
    url = 'http://localhost:4000/auth-service/verify-images?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJjb21wYW55IjoiQW1hem9uIiwiaXAiOiIxMjcuMC4wLjEiLCJleHAiOjE2NTY4OTU3MTB9.Tj8Hm6aDgF_GokVjmYFL0NLJa4jh0Sb1KWgeODcil-I'
    files = [('file', open('static\image_users\image_user.png', 'rb')),
             ('file', open('image.jpg', 'rb'))]
    # ('file', open('static\image_users\image_user.png', 'rb'))]

    response = requests.get(url, files=files, json={'key': 'value'})
    json_response = response.json()
    return json_response
