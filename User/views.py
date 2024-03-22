from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import auth,firestore,credentials
import pyrebase
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from datetime import datetime
from django.http import JsonResponse


# Create your views here.

db = firestore.client()

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


def homepage(request):
    return render(request,"User/Userhomepage.html")

def profile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    return render(request,"User/Profile.html",{"user":user})

def editprofile(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    if request.method == "POST":
        data = {"user_name":request.POST.get("txt_name"),"user_contact":request.POST.get("txt_contact"),
                "user_address":request.POST.get("txt_address")}
        db.collection("tbl_user").document(request.session["uid"]).update(data)
        return redirect("webuser:profile")
    else:
        return render(request,"User/Editprofile.html",{"user":user})

def changepassword(request):
    user = db.collection("tbl_user").document(request.session["uid"]).get().to_dict()
    email = user["user_email"]

    em_link = firebase_admin.auth.generate_password_reset_link(email)
    send_mail(
        'Reset your password ', #subject
        "\rHello \r\nFollow this link to reset your QuesPro user password for your email " + email + "\n" + em_link +".\n If you didn't ask to reset your password, you can ignore this email. \r\n Thanks. \r\n QuesPro Services.",#body
        settings.EMAIL_HOST_USER,
        [email],)
    return redirect("webuser:homepage")

def complaints(request):

    compdata = db.collection("tbl_complaint").where("user_id","==",request.session["uid"]).stream()
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
        user_id = request.session["uid"]
        data = {"user_id":user_id,
                "professional_id":"",
                "complaint_name":request.POST.get("txt_complaint"),
                "complainttype_id":request.POST.get("sel_complainttype"),
                "complaint_date":datetime.now(),
                "cstatus":0,
                "complaint_reply":"Not replied yet",
                "reply_date":"",
                }
        db.collection("tbl_complaint").add(data)
        return redirect("webuser:complaints")
    else:
        return render(request,"User/Complaints.html",{"comptypedata":comptype_data,"complaintdata":comp_data})

# def viewcomplaints(request):
#     compdata = db.collection("tbl_complaints").where("user_id","==",request.session["uid"]).stream()
#     comp_data = []
#     for c in compdata:
#         data = c.to_dict()
#         complainttype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()
#         comp_data.append({"complaint":data,"id":c.id,"com":complainttype})
#     return render(request,"User/Complaints.html",{"complaintdata":comp_data})

def feedback(request):
    # Fetch existing feedback data for the professional
    feedback = db.collection("tbl_feedback").where("user_id", "==", request.session["uid"]).stream()
    feedback_data = []

    for f in feedback:
        data = f.to_dict()
        feedback_data.append({"feedback": data, "id": f.id})

    # Handle POST request to add new feedback
    if request.method == "POST":
        new_feedback = {
            "user_id": request.session["uid"],
            "feedback_name": request.POST.get("txt_feedback"),
            "feedback_date":datetime.now(),
        }
        db.collection("tbl_feedback").add(new_feedback)
        return redirect("webuser:feedback")
    else:
        # Render the template with existing feedback data for GET requests
        return render(request, "User/Feedback.html", {"feedbackdata": feedback_data})

# SEARCH PROFESSIONALS

def searchprofessionals(request):
    profession = db.collection("tbl_profession").stream()
    profession_data = []
    for p in profession:
        data = p.to_dict()
        profession_data.append({"profession":data,"id":p.id})

    professionals = db.collection("tbl_professional").stream()
    prof_data = []
    for i in professionals:
        data = i.to_dict()
        pro = db.collection("tbl_profession").document(data["profession_id"]).get().to_dict()
        prof_data.append({
            "professional":data,
            "id":i.id,
            "pro":pro,
            "condition":requestcheck(i.id,request.session["uid"]),
            })
    return render(request,"User/Searchprofessionals.html",{"professiondata":profession_data,"pro":prof_data})

def requestcheck(pid,uid):
    procount = db.collection("tbl_request").where("professional_id", "==", pid).where("user_id", "==", uid).get()
    # print(len(procount))
    return len(procount)

def ajaxprofession(request):
    professionals = db.collection("tbl_professional").where("profession_id", "==" ,request.GET.get("prof")).stream()
    prof_data = []
    for i in professionals:
        data = i.to_dict()
        pro = db.collection("tbl_profession").document(data["profession_id"]).get().to_dict()
        prof_data.append({"professional":data,"id":i.id,"pro":pro})
    return render(request,"User/Ajaxprofessional.html",{"professionalsdata":prof_data})

def sendrequest(request,id):
    data = {"user_id":request.session["uid"],"rstatus":0,"request_date":datetime.now(),"professional_id":id}
    db.collection("tbl_request").add(data)
    return redirect("webuser:searchprofessionals")

def following(request):
    requests = db.collection("tbl_request").where("rstatus","==",0).where("user_id","==",request.session["uid"]).stream()
    request_data = []
    for i in requests:
        data = i.to_dict()
        pro = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        profession = db.collection("tbl_profession").document(pro["profession_id"]).get().to_dict()
        request_data.append({"requests":data,"id":i.id,"professional":pro,"profession":profession})

    accepted = db.collection("tbl_request").where("rstatus","==",1).where("user_id","==",request.session["uid"]).stream()
    accepted_data = []
    for j in accepted:
        data = j.to_dict()
        apro = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        aprofession = db.collection("tbl_profession").document(apro["profession_id"]).get().to_dict()
        accepted_data.append({"accepted":data,"id":j.id,"aprofessional":apro,"aprofession":aprofession})

    rejected = db.collection("tbl_request").where("rstatus","==",2).where("user_id","==",request.session["uid"]).stream()
    rejected_data = []
    for k in rejected:
        data = k.to_dict()
        rpro = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        rprofession = db.collection("tbl_profession").document(rpro["profession_id"]).get().to_dict()
        rejected_data.append({"rejected":data,"id":k.id,"rprofessional":rpro,"rprofession":rprofession})

    return render(request,"User/Following.html",{"following":request_data,"accepted":accepted_data,"rejected":rejected_data})

def professionalprofile(request,id):
    requests = db.collection("tbl_request").document(id).get().to_dict()
    professionalid = db.collection("tbl_professional").document(requests["professional_id"]).get()
    professional = db.collection("tbl_professional").document(requests["professional_id"]).get().to_dict()
    profession = db.collection("tbl_profession").document(professional["profession_id"]).get().to_dict()
    return render(request,"User/Professionalprofile.html",{"professionaldata":professional,"professiondata":profession,"id":professionalid.id})

def sendappoinment(request,id):
    if request.method == "POST":
        data = {"user_id":request.session["uid"],
                "professional_id":id,
                "appoinment_date":request.POST.get("txt_date"),
                "time_from":request.POST.get("txt_timefrom"),
                "time_to":request.POST.get("txt_timeto"),
                "appoinment_matter":request.POST.get("txt_matter"),
                "astatus":0,
                }
        db.collection("tbl_appoinment").add(data)
        return redirect("webuser:viewappoinment")
    else:
        return render(request,"User/Appoinment.html")
    
def viewappoinment(request):
    appoinment = db.collection("tbl_appoinment").where("user_id","==",request.session["uid"]).stream()
    appoinment_data = []
    for a in appoinment:
        data = a.to_dict()
        prof = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        appoinment_data.append({"appoinment":data,"id":a.id,"professional":prof})
    return render(request,"User/Viewappoinment.html",{"appoinmentdata":appoinment_data})

def post(request):
    post = db.collection("tbl_post").stream()
    post_data = []
    for i in post:
        likescount = db.collection("tbl_like").where("post_id", "==", i.id).get()
        data_list_count = len(likescount)
        # print(data_list_count)
        ps = i.to_dict()
        pro = db.collection("tbl_professional").document(ps["professional_id"]).get().to_dict()
        likes = db.collection("tbl_like").where("post_id", "==", i.id).where("user_id", "==", request.session["uid"]).get()
        data_list = len(likes)
        cc = 0
        # print(data_list)
        if data_list > 0:
            cc = cc + 1
            post_data.append({"post":i.to_dict(),"id":i.id,"pro":pro,"condition":1,"count":data_list_count})
        else:
            post_data.append({"post":i.to_dict(),"id":i.id,"pro":pro,"condition":0,"count":data_list_count})
    # print(post_data)
    
    return render(request,"User/Post.html",{"post":post_data})

def ajaxlike(request):
    count = db.collection("tbl_like").where("user_id", "==", request.session["uid"]).where("post_id", "==", request.GET.get("postid")).stream()
    ct = 0
    for c in count:
        ct = ct + 1
        id = c.id
    # print(ct)
    if ct > 0:
        db.collection("tbl_like").document(id).delete()
        likescount = db.collection("tbl_like").where("post_id", "==", request.GET.get("postid")).get()
        data_list_count = len(likescount)
        # print(data_list_count)
        return JsonResponse({"color":1,"count":data_list_count})
    else:
        db.collection("tbl_like").add({"user_id":request.session["uid"],"post_id":request.GET.get("postid")})
        likescount = db.collection("tbl_like").where("post_id", "==", request.GET.get("postid")).get()
        data_list_count = len(likescount)
        # print(data_list_count)
        return JsonResponse({"color":0,"count":data_list_count})

def ajaxcomment(request):
    db.collection("tbl_comment").add({"post_id":request.GET.get("postid"),"user_id":request.session["uid"],"command_content":request.GET.get("content")})
    comment = db.collection("tbl_comment").where("post_id", "==", request.GET.get("postid")).stream()
    com_data = []
    for c in comment:
        cm = c.to_dict()
        user = db.collection("tbl_user").document(cm["user_id"]).get().to_dict()
        com_data.append({"comment":c.to_dict(),"id":c.id,"user":user})
    return render(request,"User/AjaxComment.html",{"comment":com_data})

def ajaxgetcommant(request):
    comment = db.collection("tbl_comment").where("post_id", "==",request.GET.get("postid")).stream()
    com_data = []
    for c in comment:
        cm = c.to_dict()
        user = db.collection("tbl_user").document(cm["user_id"]).get().to_dict()
        com_data.append({"comment":c.to_dict(),"id":c.id,"user":user})
    return render(request,"User/AjaxComment.html",{"comment":com_data})


def payment(request,id):
    app = db.collection("tbl_appoinment").document(id).get().to_dict()
    pro = db.collection("tbl_professional").document(app["professional_id"]).get().to_dict()
    fee = pro["professional_fees"]
    if request.method == "POST":
        app = db.collection("tbl_appoinment").document(id).update({"astatus":3})
        return redirect("webuser:loader")
    else:
        return render(request,"User/Payment.html",{"total":fee})

def loader(request):
    return render(request,"User/Loader.html")

def paymentsuc(request):
    return render(request,"User/Payment_suc.html")


def chat(request,id):
    app = db.collection("tbl_appoinment").document(id).get().to_dict()
    to_user = db.collection("tbl_professional").document(app["professional_id"]).get().to_dict()
    return render(request,"User/Chat.html",{"user":to_user,"tid":app["professional_id"],"status":app["astatus"]})

def ajaxchat(request):
    image = request.FILES.get("file")
    tid = request.POST.get("tid")
    if image:
        path = "ChatFiles/" + image.name
        sd.child(path).put(image)
        d_url = sd.child(path).get_url(None)
        db.collection("tbl_chat").add({"chat_content":"","chat_time":datetime.now(),"user_from":request.session["uid"],"professional_to":request.POST.get("tid"),"chat_file":d_url,"user_to":"","professional_from":""})
        return render(request,"User/Chat.html",{"tid":tid})
    else:
        db.collection("tbl_chat").add({"chat_content":request.POST.get("msg"),"chat_time":datetime.now(),"user_from":request.session["uid"],"professional_to":request.POST.get("tid"),"chat_file":"","user_to":"","professional_from":""})
        return render(request,"User/Chat.html",{"tid":tid})

def ajaxchatview(request):
    tid = request.GET.get("tid")
    chat = db.collection("tbl_chat").order_by("chat_time").stream()
    data = []
    for c in chat:
        cdata = c.to_dict()
        if ((cdata["user_from"] == request.session["uid"]) | (cdata["user_to"] == request.session["uid"])) & ((cdata["professional_from"] == tid) | (cdata["professional_to"] == tid)):
            data.append(cdata)
    return render(request,"User/ChatView.html",{"data":data,"tid":tid})

def clearchat(request):
    toid = request.GET.get("tid")
    chat_data1 = db.collection("tbl_chat").where("user_from", "==", request.session["uid"]).where("professional_to", "==", request.GET.get("tid")).stream()
    for i1 in chat_data1:
        i1.reference.delete()
    chat_data2 = db.collection("tbl_chat").where("user_to", "==", request.session["uid"]).where("professional_from", "==", request.GET.get("tid")).stream()
    for i2 in chat_data2:
        i2.reference.delete()
    return render(request,"User/ClearChat.html",{"msg":"Chat Cleared Sucessfully....."})