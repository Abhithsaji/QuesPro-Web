from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import auth,firestore,credentials
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages

Config = {
  "apiKey": "AIzaSyDCGkJaaLslwxKlIDvscJi4ftbmLQX2Rns",
  "authDomain": "quespro-8d1d3.firebaseapp.com",
  "projectId": "quespro-8d1d3",
  "storageBucket": "quespro-8d1d3.appspot.com",
  "messagingSenderId": "907286605495",
  "appId": "1:907286605495:web:7f416537a80b4bfa83e732",
  "measurementId": "G-RDZGE89JVC",
  "databaseURL":""
}

firebase = pyrebase.initialize_app(Config)
authe = firebase.auth()
sd = firebase.storage()

# Create your views here.


db = firestore.client()

def index(request):
    return render(request,"Guest/index.html")

def Professionalregistration(request):

# select district

    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"district":d.to_dict(),"id":d.id})

# Select profession

    prof = db.collection("tbl_profession").stream()
    prof_data = []
    for p in prof:
        prof_data.append({"profession":p.to_dict(),"id":p.id})

    if request.method == "POST":

# Authentication

        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except(firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/Professionalregistration.html",{"msg":error})

# File upload photo

        photo = request.FILES.get("file_photo")
        if photo:
            path = "ProfessionalPhoto/" + photo.name
            sd.child(path).put(photo)
            downloadphoto_url = sd.child(path).get_url(None)
        
# File upload aadhar

        aadhar = request.FILES.get("file_aadhar")
        if aadhar:
            path = "ProfessionalProof/" + aadhar.name
            sd.child(path).put(aadhar)
            downloadaadhar_url = sd.child(path).get_url(None)

# Data Insertion

        data = {"professional_name":request.POST.get("txt_name"),"professional_email":email,"professional_contact":request.POST.get("txt_contact"),
                "professional_address":request.POST.get("txt_address"),"place_id":request.POST.get("sel_place"),"professional_photo":downloadphoto_url,
                "professional_proof":downloadaadhar_url,"profession_id":request.POST.get("sel_profession"),"professional_about":request.POST.get("txt_about"),
                "professional_id":user.uid,"professional_specification":request.POST.get("txt_specification"),"professional_aadharno":request.POST.get("txt_aadharno"),"vstatus":0,
                "professional_gender":request.POST.get("rad_gender"),"professional_dob":request.POST.get("date_dob"),"professional_fees":request.POST.get("txt_fees")}
        db.collection("tbl_professional").add(data)
        return render(request,"Guest/Professionalregistration.html")
    else:
        return render(request,"Guest/Professionalregistration.html",{"districtdata":dis_data,"profession_data":prof_data})


def userregistration(request):
    
    #select district

    dis = db.collection("tbl_district").stream()
    dis_data = []
    for d in dis:
        dis_data.append({"district":d.to_dict(),"id":d.id})


    if request.method == "POST":

        # Authentication

        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")
        confpass = request.POST.get("txt_confpass")

        
        try:
            user = firebase_admin.auth.create_user(email=email,password=password)
        except(firebase_admin._auth_utils.EmailAlreadyExistsError,ValueError) as error:
            return render(request,"Guest/Userregistration.html",{"msg":error})

        # FILE upload

        image = request.FILES.get("file_photo")
        if image:
            path = "Photo/" + image.name
            sd.child(path).put(image)
            download_url = sd.child(path).get_url(None)


        # Data Insertion
        
        data = {"user_name":request.POST.get("txt_name"),"user_email":email,"user_contact":request.POST.get("txt_contact"),
        "user_address":request.POST.get("txt_address"),"user_gender":request.POST.get("rad_gender"),"user_dob":request.POST.get("date_dob"),
        "place_id":request.POST.get("sel_place"),"photo_url":download_url,"user_id":user.uid,"vstatus":1}
        
        db.collection("tbl_user").add(data)
        return render(request,"Guest/Userregistration.html")

        
    else:
        return render(request,"Guest/Userregistration.html",{"district_data":dis_data})

def ajaxplace(request):
    place = db.collection("tbl_place").where("district_id", "==" ,request.GET.get("disd")).stream()
    place_data = []
    for p in place:
        place_data.append({"place":p.to_dict(),"id":p.id})
    return render(request,"Guest/Ajaxplace.html",{"place":place_data})

def login(request):
    udata_id = ""
    pdata_id = ""

    if request.method == "POST":
        email = request.POST.get("txt_email")
        password = request.POST.get("txt_password")

        # ADMIN 
         
        if (email == "quesproservice@gmail.com") & (password == "123456"):
            request.session["aid"] = 1
            return redirect("webadmin:adminhomepage")
        else:
            try:
                user = authe.sign_in_with_email_and_password(email,password)
            except: 
                return render(request,"Guest/Login.html",{'msg':"INVALID_LOGIN_CREDENTIALS... Check Email and Password"})
            
            userid = user["localId"]

            # USER
            user_data = db.collection("tbl_user").where("user_id", "==", userid).stream()
            for i in user_data:
                data = i.to_dict()
                udata_id = i.id
                vstatusu = data["vstatus"]

            # PROFESSIONAL
        
            prof_data = db.collection("tbl_professional").where("professional_id", "==", userid).stream()
            for p in prof_data:
                data = p.to_dict()
                pdata_id = p.id
                vstatusp = data["vstatus"]
                
            
            if udata_id:
                if vstatusu == 1:
                    request.session["uid"] = udata_id
                    return redirect("webuser:homepage")
                elif vstatusu == 2:
                    return render(request,"Guest/Login.html",{"msg":"Registration Rejected"})
                else:
                    return render(request,"Guest/Login.html",{"msg":"Registration pending"})

            elif pdata_id:
                if vstatusp == 1:
                    request.session['pid'] = pdata_id
                    return redirect("webprofessionals:homepageprofessional")
                elif vstatusp == 2:
                    return render(request,"Guest/Login.html",{"msg":"Registration Rejected"})
                else:
                    return render(request,"Guest/Login.html",{"msg":"Registration pending"})

            else: 
                return render(request,"Guest/Login.html",{"msg":"Your Request is pending or Rejected"})
    else:
        return render(request,"Guest/Login.html")

def fpassword(request):
    if request.method == "POST":
        email = request.POST.get("txt_email")
        reset_link = firebase_admin.auth.generate_password_reset_link(email)
        send_mail(
            'Forgot password ', #subject
            "\rHello \r\nFollow this link to reset your QuesPro password for your " + email + "\n Link" + reset_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n Your D MARKET team.",#body
            settings.EMAIL_HOST_USER,
            [email],
        )
        return render(request,"Guest/Forgotpassword.html",{"msg":email})
    else:
        return render(request,"Guest/Forgotpassword.html")

