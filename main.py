import time

import cv2

import os

import pyrebase


def cls():
    print("\n"* 15)


def main():

    def doorUnlock():
        print("Door is open!")
        time.sleep(3)
        cls()
        main()

    s = int(input("Sensor:"))

    if s == 1:
        doorUnlock()

    while True:

        firebaseConfig = {
            'apiKey': "",
            'authDomain': "",
            'databaseURL': "",
            'projectId': "",
            'storageBucket': "",
            'messagingSenderId': "",
            'appId': "",
            'measurementId': ""
        }


        firebase = pyrebase.initialize_app(firebaseConfig)

        storage = firebase.storage()

        database = firebase.database()

        print("Starting Camera...")

        time.sleep(2)

        cls()

        # os.system('clear')

        cap = cv2.VideoCapture(0)

        print("Camera Started...")

        time.sleep(2)

        cls()

        while True:

            _, img = cap.read()

            k = cv2.waitKey(10) & 0xff

            cv2.imshow('img', img)

            t = time.strftime("%Y-%m-%d_%H-%M-$S")

            if s == 0:                    # if k == ord('c') or k == ord('C'):
                print("\n\nWelcome to SGBIT.\nPlease wear yor mask and maintain social distancing.")
                print("Scan your ID card...")
                time.sleep(3)
                usn = input("Enter yor USN: ")
                temp = int(input("Enter your Temperature: "))

                if temp <= 37:
                    p = 'AG'
                    file = usn+'_'+str(temp)+'°C_'+p+'_'+t+'.jpeg'
                    print("Capturing Image...")
                    time.sleep(3)
                    cv2.imwrite(file, img)
                    cv2.imread(file)
                    print("Image Captured")
                    print("Access Granted!")
                    storage.child(file).put(file)
                    url = storage.child(file).get_url(file)
                    data = {"USN" : usn, "Temperature" : str(temp)+"℃", "TimeStamp" : t,  "Access" : p, "Image" : file, "ImgURL" : url}
                    database.child("Attendance").push(data)
                    os.remove(file)
                    doorUnlock()

                else:
                    p = 'AD'
                    file = usn+'_'+str(temp)+'C_'+p+'_'+t+'.jpeg'
                    print("Capturing Image...")
                    time.sleep(3)
                    cv2.imwrite(file, img)
                    cv2.imread(file)
                    print("Image Captured")
                    print("Access Denied!")
                    storage.child(file).put(file)
                    url = storage.child(file).get_url(file)
                    data = {"USN" : usn, "Temperature" : str(temp)+"℃", "TimeStamp" : t,  "Access" : p, "Image" : file, "ImgURL" : url}
                    database.child("Attendance").push(data)
                    os.remove(file)
                    cls()
                    main()

            elif k == ord("q"):
                print("Closing the window.\nBye!")
                exit()


main()






