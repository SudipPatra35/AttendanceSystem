import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred,{
    'databaseURL':"https://faceattendancesystem-415c2-default-rtdb.firebaseio.com/"
})

ref=db.reference('Employees')


details={
    "123454" : {
        "name" : "Mr. Narendra Modi",
        "post" : "Senior SE",
        "email":"narendra.modi@gamil.com",
        "phone" : "9654135656" ,
        "TotalAttendance" : 41,
        "LastAttendance" : "2024-10-08"
    },
    "123455" : {
        "name" : "Sudip Patra",
        "post" : "Junior SE",
        "email":"sudip.patra@gamil.com",
        "phone" : "9654189456" ,
        "TotalAttendance" : 15,
        "LastAttendance" : "2024-10-09"
    },
    "123456" : {
        "name" : "Mr. Ratan Tata",
        "post" : "CEO",
        "email":"sirratan.tata@gamil.com",
        "phone" : "9654181023" ,
        "TotalAttendance" : 75,
        "LastAttendance" : "2024-10-08"
    },
    "123457" : {
        "name" : "Mr. Elon Musk",
        "post" : "Manager",
        "email":"elon.musk@gamil.com",
        "phone" : "9654120465" ,
        "TotalAttendance" : 55,
        "LastAttendance" : "2024-10-08"
    },
    "123458" : {
        "name" : "Mr. Leo Messi",
        "post" : "Product Designer",
        "email":"leo.messi@gamil.com",
        "phone" : "9655601238" ,
        "TotalAttendance" : 29,
        "LastAttendance" : "2024-10-09"
    },
    "123459" : {
        "name" : "Mr. Sunil Chhetri",
        "post" : "System Developer",
        "email":"chhetri.sunil@gamil.com",
        "phone" : "8945789632" ,
        "TotalAttendance" : 32,
        "LastAttendance" : "2024-10-08"
    },
    "123460" : {
        "name" : "Soumodip Patra",
        "post" : "SE Intern",
        "email":"soumo.patra@gamil.com",
        "phone" : "9875413884" ,
        "TotalAttendance" : 6,
        "LastAttendance" : "2024-10-09"
    },
}
for key,value in details.items():
    ref.child(key).set(value)
