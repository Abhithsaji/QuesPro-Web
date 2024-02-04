from django.shortcuts import render,redirect
import firebase_admin
from firebase_admin import auth,firestore,credentials
import pyrebase
from datetime import datetime


# Create your views here.

db = firestore.client()

#add district

def district(request):

    #print data in tbl_district

    dis = db.collection("tbl_district").stream()
    dis_data = []
    for i in dis:
        data = i.to_dict()
        dis_data.append({"District":data,"id":i.id})

    # Insert data 

    if request.method == "POST":
        data = {"district_name":request.POST.get("txt_district")}
        db.collection("tbl_district").add(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"dis":dis_data})

#  delete district

def deldistrict(request,id):
    dis = db.collection("tbl_district").document(id).delete()
    return redirect("webadmin:district")
 
# update district

def updatedistrict(request,id):
    dis = db.collection("tbl_district").document(id).get().to_dict()
    if request.method == "POST":
        data = {"district_name":request.POST.get("txt_district")}
        db.collection("tbl_district").document(id).update(data)
        return redirect("webadmin:district")
    else:
        return render(request,"Admin/District.html",{"district":dis})

# Inser place

def place(request):
    district = db.collection("tbl_district").stream()
    district_data = []

    for i in district:
        data = i.to_dict()
        district_data.append({"district":data,"id":i.id})
    
    place = db.collection("tbl_place").stream()
    place_data = []
    for j in place:
        pdata = j.to_dict()
        dis_id = pdata["district_id"]
        placedata = db.collection("tbl_district").document(dis_id).get()
        disdata = placedata.to_dict()
        place_data.append({"district":disdata,"place":pdata,"id":j.id})
    
    if request.method == "POST":
        data = {"place_name":request.POST.get("txt_place"),"district_id":request.POST.get("sel_district")}
        db.collection("tbl_place").add(data)
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/Place.html",{"place":place_data,"district":district_data})

# delete place

def delplace(request,id):
    db.collection("tbl_place").document(id).delete()
    return redirect("webadmin:place")

# Update place

def updateplace(request,id):
    district = db.collection("tbl_district").stream()
    dist_data = []
    for c in district:
        dist_data.append({"district":c.to_dict(),"id":c.id})

    place = db.collection("tbl_place").document(id).get().to_dict()
    if request.method == "POST":
        data = {"place_name":request.POST.get("txt_place")}
        db.collection("tbl_place").document(id).update(data)
        return redirect("webadmin:place")
    else:
        return render(request,"Admin/place.html",{"placedata":place,"district":dist_data})

def profession(request):

    #print data in tbl_district

    profession = db.collection("tbl_profession").stream()
    prof_data = []
    for i in profession:
        data = i.to_dict()
        prof_data.append({"Profession":data,"id":i.id})

    # Insert data 

    if request.method == "POST":
        data = {"profession_name":request.POST.get("txt_profession")}
        db.collection("tbl_profession").add(data)
        return redirect("webadmin:profession")
    else:
        return render(request,"Admin/Profession.html",{"profession":prof_data})

# Delete profession

def delprofession(request,id):
    db.collection("tbl_profession").document(id).delete()
    return redirect("webadmin:profession")

# Update Profession

def updateprofession(request,id):
    profession = db.collection("tbl_profession").document(id).get().to_dict()
    if request.method == "POST":
        data = {"profession_name":request.POST.get("txt_profession")}
        db.collection("tbl_profession").document(id).update(data)
        return redirect("webadmin:profession")
    else:
        return render(request,"Admin/Profession.html",{"profession_data":profession})

# Insert complaint type'

def comptype(request):

    #print data in tbl_district

    comptype = db.collection("tbl_complainttype").stream()
    comptype_data = []
    for i in comptype:
        data = i.to_dict()
        comptype_data.append({"comptype":data,"id":i.id})

    # Insert data 

    if request.method == "POST":
        data = {"complainttype_name":request.POST.get("txt_comptype")}
        db.collection("tbl_complainttype").add(data)
        return redirect("webadmin:comptype")
    else:
        return render(request,"Admin/Complainttype.html",{"comptype":comptype_data})

# Delete profession

def delcomptype(request,id):
    db.collection("tbl_complainttype").document(id).delete()
    return redirect("webadmin:comptype")

# Update Profession

def updatecomptype(request,id):
    comptype = db.collection("tbl_complainttype").document(id).get().to_dict()
    if request.method == "POST":
        data = {"complainttype_name":request.POST.get("txt_comptype")}
        db.collection("tbl_complainttype").document(id).update(data)
        return redirect("webadmin:comptype")
    else:
        return render(request,"Admin/Complainttype.html",{"comptype_data":comptype})

def adminhomepage(request):
    return render(request,"Admin/Adminhomepage.html")

# VIEW New User

def newuser(request):
    user = db.collection("tbl_user").stream()
    user_data = []
    for u in user:
        data = u.to_dict()
        user_data.append({"user":data,"id":u.id})
    return render(request,"Admin/Newuser.html",{"userdata":user_data})

# REJECT User

# def rejectuser(request,id):
#     data = {"vstatus":2}
#     db.collection("tbl_user").document(id).update(data)
#     return redirect("webadmin:adminhomepage")

# # APROVE User

# def approveuser(request,id):
#     data = {"vstatus":1}
#     db.collection("tbl_user").document(id).update(data)
#     return redirect("webadmin:adminhomepage")


# # ACCEPTED User

# def accepteduser(request):
#     user = db.collection("tbl_user").where("vstatus","==",1).stream()
#     user_data = []
#     for u in user:
#         data = u.to_dict()
#         user_data.append({"user":data,"id":u.id})
#     return render(request,"Admin/Accepteduser.html",{"auserdata":user_data})
    

# # REJECTED User

# def rejecteduser(request):
#     user = db.collection("tbl_user").where("vstatus","==",2).stream()
#     user_data = []
#     for u in user:
#         data = u.to_dict()
#         user_data.append({"user":data,"id":u.id})
#     return render(request,"Admin/Rejecteduser.html",{"ruserdata":user_data})

# NEW PROFESSIONALS

def newprofessionals(request):
    prof = db.collection("tbl_professional").where("vstatus", "==", 0).stream()
    prof_data = []
    for p in prof:
        data = p.to_dict()
        pro = db.collection("tbl_profession").document(data["profession_id"]).get().to_dict()
        prof_data.append({"professional":data,"id":p.id,"prof_name":pro})
        return render(request,"Admin/Newprofessionals.html",{"profdata":prof_data})
    else:
        return render(request,"Admin/Newprofessionals.html")

def aproveprofessionals(request,id):
    data = {"vstatus":1}
    db.collection("tbl_professional").document(id).update(data)
    return redirect("webadmin:adminhomepage")
    
def rejectprofessionals(request,id):
    data = {"vstatus":2}
    db.collection("tbl_professional").document(id).update(data)
    return redirect("webadmin:adminhomepage")

def aprovedprofessionals(request):
    prof = db.collection("tbl_professional").where("vstatus", "==", 1).stream()
    prof_data = []
    for p in prof:
        data = p.to_dict()
        pro = db.collection("tbl_profession").document(data["profession_id"]).get().to_dict()
        prof_data.append({"professional":data,"id":p.id,"prof_name":pro})
    return render(request,"Admin/Approvedprofessionals.html",{"approveddata":prof_data})


    
def rejectedprofessionals(request):
    prof = db.collection("tbl_professional").where("vstatus", "==", 2).stream()
    prof_data = []
    for p in prof:
        data = p.to_dict()
        pro = db.collection("tbl_profession").document(data["profession_id"]).get().to_dict()
        prof_data.append({"professional":data,"id":p.id,"prof_name":pro})
    return render(request,"Admin/Rejectedprofessionals.html",{"rejecteddata":prof_data})

# COMPLAINTS USER

def complaints(request):

# USER COMPLAINTS
    usercomplaints = db.collection("tbl_complaint").where("user_id","!=",0).where("cstatus","==",0).stream()
    comp_user = []
    for c in usercomplaints :
        data = c.to_dict()
        # INNER JOIN COMPLAINT TYPE

        ctype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()

        # INNER JOIN USER NAME

        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()

        comp_user.append({"usercomplaints":data,"id":c.id,"ucomplainttype":ctype,"username":user})
    # print(comp_user)


    # PROFESSIONALS COMPLAINT
    professionalcomplaints = db.collection("tbl_complaint").where("professional_id","!=","").where("cstatus","==",0).stream()
    comp_prof = []
    for d in professionalcomplaints :
        data = d.to_dict()
        # INNER JOIN COMPLAINT TYPE
        ctype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()
        # INNER JOIN USER NAME
        prof = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        comp_prof.append({"profcomplaints":data,"id":d.id,"pcomplainttype":ctype,"profname":prof})
    
    return render(request,"Admin/Complaints.html",{"ucomplaintdata":comp_user,"pcomplaintdata":comp_prof,})

def repliedcomplaint(request):

# USER COMPLAINTS

    usercomplaints = db.collection("tbl_complaint").where("user_id","!=","").where("cstatus","==",1).stream()
    comp_user = []
    for c in usercomplaints :
        data = c.to_dict()
        # INNER JOIN COMPLAINT TYPE

        uctype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()

        # INNER JOIN USER NAME

        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()

        comp_user.append({"usercomplaints":data,"id":c.id,"ucomplainttype":uctype,"username":user})


# PROFESSIONALS COMPLAINT
    professionalcomplaints = db.collection("tbl_complaint").where("professional_id","!=","").where("cstatus","==",1).stream()
    comp_prof = []
    for d in professionalcomplaints :
        data = d.to_dict()
        # INNER JOIN COMPLAINT TYPE
        ctype = db.collection("tbl_complainttype").document(data["complainttype_id"]).get().to_dict()
        # INNER JOIN USER NAME
        prof = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()
        comp_prof.append({"profcomplaints":data,"id":d.id,"pcomplainttype":ctype,"profname":prof})
    
    return render(request,"Admin/Repliedcomplaints.html",{"urcomplaintdata":comp_user,"prcomplaintdata":comp_prof,})


def replycomplaints(request,id):
    db.collection("tbl_complaint").document(id).get().to_dict()
    if request.method == "POST":
        data = {"complaint_reply":request.POST.get("txt_reply"),"cstatus":1,"reply_date":datetime.now()}
        db.collection("tbl_complaint").document(id).update(data)
        return render(request,"Admin/Replycomplaints.html", {"msg":"Replied Successfully...."})
    else:
        return render(request,"Admin/Replycomplaints.html")



def feedback(request):
    feedbackprof = db.collection("tbl_feedback").where("professional_id","!=",0).stream()
    feedback_prof = []
    for k in feedbackprof:
        data = k.to_dict()

        prof = db.collection("tbl_professional").document(data["professional_id"]).get().to_dict()

        feedback_prof.append({"feedback":data,"id":k.id,"professionalname":prof})

    feedbackuser = db.collection("tbl_feedback").where("user_id","!=",0).stream()
    feedback_user = []
    for f in feedbackuser:
        data = f.to_dict()

        user = db.collection("tbl_user").document(data["user_id"]).get().to_dict()

        feedback_user.append({"feedback":data,"id":f.id,"username":user})

    return render(request,"Admin/Professionalfeedback.html",{"prof_feedback":feedback_prof,"userfeedback":feedback_user})


