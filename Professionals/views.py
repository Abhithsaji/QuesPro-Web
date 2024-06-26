from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import auth,firestore,credentials
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime

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

def homepage(request):
    if 'pid' in request.session:
        return render(request,"Professionals/Homepageprofessional.html")
    else:
        return redirect("webguest:login")

def profile(request):
    professional = db.collection("tbl_professional").document(request.session['pid']).get().to_dict()
    return render(request,"Professionals/Profile.html",{"professional":professional})

def editprofile(request):
    prof = db.collection("tbl_professional").document(request.session["pid"]).get().to_dict()
    if request.method == "POST":
        data = {"professional_name":request.POST.get("txt_name"),"professional_contact":request.POST.get("txt_contact"),
                "professional_address":request.POST.get("txt_address"),"professional_about":request.POST.get("txt_about"),"professional_fees":request.POST.get("txt_fees")}
        db.collection("tbl_professional").document(request.session["pid"]).update(data)
        return redirect("webprofessionals:profile")
    else:
        return render(request,"Professionals/Editprofile.html",{"professional":prof})

def changepassword(request):
    prof = db.collection("tbl_professional").document(request.session["pid"]).get().to_dict()
    email = prof["professional_email"]

    em_link = firebase_admin.auth.generate_password_reset_link(email)   
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your QuesPro Professionals password for your email " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n GuestPro Services.",#body
        settings.EMAIL_HOST_USER,
        [email],)
    return redirect("webprofessionals:homepageprofessional")

def complaints(request):
    compdata = db.collection("tbl_complaint").where("professional_id","==",request.session["pid"]).stream()
    comp_data = []
    for c in compdata:
        data = c.to_dict()
        complainttype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()
        comp_data.append({"complaint":data,"id":c.id,"com":complainttype})

    comptype = db.collection("tbl_complainttype").stream()
    comptype_data = []
    for i in comptype:
        data = i.to_dict()
        comptype_data.append({"complainttype":data,"id":i.id})
    if request.method == "POST":
        pid = request.session["pid"]
        data = {"user_id":"",
                "professional_id":pid,
                "complaint_name":request.POST.get("txt_complaint"),
                "complainttype_id":request.POST.get("sel_complainttype"),
                "complaint_date":datetime.now(),
                "cstatus":0,
                "complaint_reply":"Not replied yet",
                "reply_date":"",
                }
        db.collection("tbl_complaint").add(data)
        return redirect("webprofessionals:complaints")
    else:
        return render(request,"Professionals/Complaints.html",{"comptypedata":comptype_data,"complaintdata":comp_data})



def feedback(request):
    # Fetch existing feedback data for the professional
    feedback = db.collection("tbl_feedback").where("professional_id", "==", request.session["pid"]).stream()
    feedback_data = []

    for f in feedback:
        data = f.to_dict()
        feedback_data.append({"feedback": data, "id": f.id})

    # Handle POST request to add new feedback
    if request.method == "POST":
        new_feedback = {
            "professional_id": request.session["pid"],
            "feedback_name": request.POST.get("txt_feedback"),
            "feedback_date":datetime.now(),
        }
        db.collection("tbl_feedback").add(new_feedback)
        return redirect("webprofessionals:feedback")
    else:
        # Render the template with existing feedback data for GET requests
        return render(request, "Professionals/Feedback.html", {"feedbackdata": feedback_data})

def newrequest(request):
    pid = request.session["pid"]
    requests_query = db.collection("tbl_request").where("professional_id", "==", pid).where("rstatus","==",0).stream()
    request_data = []
    for r in requests_query:
        data = r.to_dict()
        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()
        request_data.append({"requests": data, "id": r.id, "username": user})
    
    return render(request, "Professionals/Newrequest.html", {"requestdata": request_data})


def acceptrequest(request,id):
    data = {"rstatus":1}
    db.collection("tbl_request").document(id).update(data)
    return redirect("webprofessionals:homepageprofessional")

def rejectrequest(request,id):
    data = {"rstatus":2}
    db.collection("tbl_request").document(id).update(data)
    return redirect("webprofessionals:homepageprofessional")

def acceptedrequest(request):
    pid = request.session["pid"]
    acceptrequests = db.collection("tbl_request").where("professional_id", "==", pid).where("rstatus","==",1).stream()
    accepted_request = []
    for a in acceptrequests:
        data = a.to_dict()
        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()
        accepted_request.append({"requests": data, "id": a.id, "username": user})
    
    return render(request, "Professionals/Acceptedrequest.html", {"acceptedrequest": accepted_request})

def rejectedrequest(request):
    pid = request.session["pid"]
    rejectedrequest = db.collection("tbl_request").where("professional_id", "==", pid).where("rstatus","==",2).stream()
    rejected_requst = []
    for b in rejectedrequest:
        data = b.to_dict()
        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()
        rejected_requst.append({"requests": data, "id": b.id, "username": user})
    
    return render(request, "Professionals/Rejectedrequest.html", {"rejectedrequest": rejected_requst})

def viewappoinments(request):
    appoinment = db.collection("tbl_appoinment").where("professional_id","==",request.session["pid"]).where("astatus","==",0).stream()
    appoinment_data = []
    for i in appoinment:
        data = i.to_dict()
        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()
        appoinment_data.append({"appoinment":data,"id":i.id,"userdata":user})

    aappoinment = db.collection("tbl_appoinment").where("professional_id","==",request.session["pid"]).where("astatus","!=",2).where("astatus",">=",1).stream()
    aappoinment_data = []
    for a in aappoinment:
        adata = a.to_dict()
        auser = db.collection("tbl_user").document(adata["user_id"]).get().to_dict()
        aappoinment_data.append({"aappoinment":adata,"id":a.id,"auserdata":auser})

    rappoinment = db.collection("tbl_appoinment").where("professional_id","==",request.session["pid"]).where("astatus","==",2).stream()
    rappoinment_data = []
    for r in rappoinment:
        rdata = r.to_dict()
        ruser = db.collection("tbl_user").document(rdata["user_id"]).get().to_dict()
        rappoinment_data.append({"rappoinment":rdata,"id":r.id,"ruserdata":ruser})
        
    return render(request,"Professionals/Viewappoinments.html",{"appoinmentdata":appoinment_data,"aappoinmentdata":aappoinment_data,"rappoinmentdata":rappoinment_data})
 
def acceptappoinment(request,id):
    data = {"astatus":1}
    db.collection("tbl_appoinment").document(id).update(data)
    return redirect("webprofessionals:viewappoinments")

def rejectappoinment(request,id):
    data = {"astatus":2}
    db.collection("tbl_appoinment").document(id).update(data)
    return redirect("webprofessionals:viewappoinments")


def post(request):
    post = db.collection("tbl_post").where("professional_id","==",request.session["pid"]).stream()
    post_data = []
    for i in post:
        data = i.to_dict()
        post_data.append({"post":data,"id":i.id})

    if request.method == "POST":
        post = request.FILES.get("file_post")
        if post:
            path = "Posts/" + post.name
            sd.child(path).put(post)
            downloadpost_url = sd.child(path).get_url(None)

        data = {"post_url":downloadpost_url,
                "post_date":datetime.now(),
                "post_caption":request.POST.get("txt_caption"),
                "professional_id":request.session["pid"]}
        db.collection("tbl_post").add(data)
        return redirect("webprofessionals:post")
    else:
        return render(request,"Professionals/Posts.html",{"postdata":post_data})

def delpost(request,id):
    post = db.collection("tbl_post").document(id).delete()
    return redirect("webprofessionals:post")


def chat(request,id):
    app = db.collection("tbl_appoinment").document(id).get().to_dict()
    to_user = db.collection("tbl_user").document(app["user_id"]).get().to_dict()
    return render(request,"Professionals/Chat.html",{"user":to_user,"tid":app["user_id"]})

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        sd.child(path).put(image)
        d_url = sd.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"professional_from":request.session["pid"],"user_to":request.POST.get("tid"),"chat_file":d_url,"professional_to":"","user_from":""})
        return render(request,"Professionals/Chat.html",{"tid":tid})
    else:
        db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"professional_from":request.session["pid"],"user_to":request.POST.get("tid"),"chat_file":"","professional_to":"","user_from":""})
        return render(request,"Professionals/Chat.html",{"tid":tid})

def ajaxchatview(request):
    tid = request.GET.get("tid")
    user_ref = db.collection("tbl_chat")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["professional_from"] == request.session["pid"]) | (cdata["professional_to"] == request.session["pid"])) & ((cdata["user_from"] == tid) | (cdata["user_to"] == tid)):
            data.append(cdata)
    return render(request,"Professionals/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat").where("professional_from", "==", request.session["pid"]).where("user_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat").where("professional_to", "==", request.session["pid"]).where("user_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"Professionals/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})

def endsession(request,id):
    db.collection("tbl_appoinment").document(id).update({"astatus":4})
    return redirect("webprofessionals:viewappoinments")

def logout(request):
    if 'pid' in request.session:
        request.session.pop("pid")
        return redirect("webguest:login")
    else:
        return redirect("webguest:login")