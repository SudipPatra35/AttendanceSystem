import cv2
import face_recognition
import pickle
import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
from firebase_admin import storage

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-415c2-default-rtdb.firebaseio.com/",
    'storageBucket' : "faceattendancesystem-415c2.appspot.com"
})

def findEncoding(imgList):
    encodeList = []
    for img in imgList:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img)

        # Check if at least one face was detected in the image
        if len(encodings) > 0:
            encodeList.append(encodings[0])  # Only take the first face encoding if multiple are found
        else:
            print("Warning: No face detected in one of the images.")
            encodeList.append(None)  # Handle no face case

    return encodeList

folderPath = "images"
pathList = os.listdir(folderPath)
imgList = []
empId = []

for i in pathList:
    imgList.append(cv2.imread(os.path.join(folderPath, i)))
    empId.append(os.path.splitext(i)[0])

    #Upload images to Storage : 
    filename=f'{folderPath}/{i}'
    bucket=storage.bucket()
    blob=bucket.blob(filename)
    blob.upload_from_filename(filename)
    
# print(len(imgList))
# print(empId)

print("Encoding Started...")
encodeList = findEncoding(imgList)

# Handle invalid encodings (None values)
encodeListWithIds = []
validEmpIds = []

for i, encode in enumerate(encodeList):
    if encode is not None:
        encodeListWithIds.append(encode)
        validEmpIds.append(empId[i])

print("Encoding completed")

# Save the valid encodings and corresponding employee IDs
with open("EncodedFile.p", 'wb') as file:
    pickle.dump([encodeListWithIds, validEmpIds], file)

print("File saved")
