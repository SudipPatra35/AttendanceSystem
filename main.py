import cv2
import pickle
import os
import face_recognition as fr
import numpy as np
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage
from datetime import datetime


cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-415c2-default-rtdb.firebaseio.com/",
    'storageBucket' : "faceattendancesystem-415c2.appspot.com"
})
bucket=storage.bucket()

# Load Haar Cascade for face detection
face_cap = cv2.CascadeClassifier("C:/users/sudip/appdata/local/programs/python/python312/lib/site-packages/cv2/data/haarcascade_frontalface_default.xml")

# Open webcam
cap = cv2.VideoCapture(0)
cap.set(3, 1280)  # Width
cap.set(4, 720)   # Height

# Load background 
bg = cv2.imread("resources/bg.png")

# Importing mode images
modes = "resources/Modes"
modePathList = os.listdir(modes)
imgList = []

count=0
modeType=0
id=-1
imgEmp=[]

for i in modePathList:
    imgList.append(cv2.imread(os.path.join(modes, i)))

# Load encoded file
# print("Loading Encoded file ....")
with open("EncodedFile.p", 'rb') as file:
    encodeListWithIds = pickle.load(file)
    encodeListKnown, empId = encodeListWithIds
# print("Encoded File Loaded..")


# Capturing video
while True:
    ret, img = cap.read()

    # Convert to grayscale for Haar Cascade
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Detect faces using Haar Cascade
    faces = face_cap.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(30, 30),
        flags=cv2.CASCADE_SCALE_IMAGE
    )
    
    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)

    # Convert OpenCV face coordinates (x, y, w, h) to (top, right, bottom, left) for face_recognition
    faceCurrFrame = [(y, x+w, y+h, x) for (x, y, w, h) in faces]

    # Encode the faces in the current frame
    encodeCurrFrame = fr.face_encodings(img, faceCurrFrame)
    
    # Copy the webcam image into the background
    try:
        # Ensure the dimensions match before copying
        bg[162:162+480, 85:85+640] = cv2.resize(img, (640, 480))
        bg[159:159+494, 884:884+320] = cv2.resize(imgList[modeType], (320, 494))
    except ValueError as e:
        print(f"Error while copying images: {e}")
        break

    # Face matching
    if faceCurrFrame:
        for encodeFace, faceLoc in zip(encodeCurrFrame, faceCurrFrame):
            matches = fr.compare_faces(encodeListKnown, encodeFace)
            faceDis = fr.face_distance(encodeListKnown, encodeFace)

            # Check if faceDis is non-empty and has valid data
            if len(faceDis) > 0:
                matchIndex = np.argmin(faceDis)

                # Verify that matchIndex is within bounds of matches list
                if len(matches) > matchIndex and matches[matchIndex] :
                    if count==0:
                        count=1
                        modeType=1
                    # print(f"Matched employee ID: {empId[matchIndex]}") 
                    id=empId[matchIndex] 
            #     else:
            #         print("No match found or face distance too large.")
            # else:
            #     print("No faces detected or no valid encodings.")
        
        # Print the details :
        if count!=0:
            if count==1:
                empInfo=db.reference(f'Employees/{id}').get()
                # print(empInfo['TotalAttendance'])
            
            # Print the img of emp :
                blob=bucket.get_blob(f'images/{id}.png')
                arr=np.frombuffer(blob.download_as_string(),np.uint8)
                imgEmp=cv2.imdecode(arr,cv2.COLOR_BGRA2BGR)
            # Update the student data: 
                prevTime=datetime.strptime(empInfo['LastAttendance'],"%Y-%m-%d %H:%M:%S")
                timeDiff=(datetime.now()-prevTime).total_seconds()
                # print(timeDiff)
                if timeDiff>=100:
                    ref = db.reference(f'Employees/{id}')
                    empInfo['TotalAttendance']+=1
                    ref.child('TotalAttendance').set(empInfo['TotalAttendance'])
                    ref.child('LastAttendance').set(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    modeType=3
                    count=0
                    bg[159:159+494, 884:884+320] = cv2.resize(imgList[modeType], (320, 494))

            
            if modeType!=3:    
                if 12<count<20:
                    modeType=4
                    bg[159:159+494, 884:884+320] = cv2.resize(imgList[modeType], (320, 494))
            
                if count<12:    
                    # Print the details of Employee   
                    cv2.putText(bg,str(empInfo['TotalAttendance']),(940,210),
                                        cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),1)
                
                    cv2.putText(bg,str(id),(976,525),
                                        cv2.FONT_HERSHEY_SIMPLEX,0.46,(0,0,0),1)
                    cv2.putText(bg,str(empInfo['email']),(976,549),
                                        cv2.FONT_HERSHEY_SIMPLEX,0.46,(0,0,0),1)
                    cv2.putText(bg,str(empInfo['phone']),(976,577),
                                        cv2.FONT_HERSHEY_SIMPLEX,0.46,(0,0,0),1)
                        
                    (w,h),_=cv2.getTextSize(empInfo['name'],cv2.FONT_HERSHEY_COMPLEX,0.75,1)
                    offset=1043-(w//2)
                    cv2.putText(bg,str(empInfo['name']),(offset,450),
                                        cv2.FONT_HERSHEY_COMPLEX,0.75,(0,0,0),1)
                    
                    (w,h),_=cv2.getTextSize(empInfo['post'],cv2.FONT_HERSHEY_COMPLEX,0.55,1)
                    offset=1043-(w//2)
                    cv2.putText(bg,str(empInfo['post']),(offset,476),
                                        cv2.FONT_HERSHEY_COMPLEX,0.55,(0,0,0),1)
                    
                    bg[277:277+125,970:970+147]=imgEmp
                
            count+=1
            if count>=20:
                count=0
                modeType=0
                id=-1
                imgEmp=[]
                empInfo=[]
                bg[159:159+494, 884:884+320] = cv2.resize(imgList[modeType], (320, 494))
    else:
        modeType=0
        count=0
    # Display the result
    cv2.imshow("Capturing Face", bg)
    # Exit on pressing 'q'
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
# 1040,264