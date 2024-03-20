from django.urls import path,include
from Admin import views
app_name = 'webadmin'

urlpatterns = [
    path('District/',views.district,name="district"),

    path('deldistrict/<str:id>',views.deldistrict,name="deldistrict"),
    path('updatedistrict/<str:id>',views.updatedistrict,name="updatedistrict"),

    path('Place/',views.place,name="place"),

    path('delplace/<str:id>',views.delplace,name="delplace"),
    path('updateplace/<str:id>',views.updateplace,name="updateplace"),

    path('Profession/',views.profession,name="profession"),

    path('delprofession/<str:id>',views.delprofession,name="delprofession"),
    path('updateprofession/<str:id>',views.updateprofession,name="updateprofession"),

    path('Complainttype/',views.comptype,name="comptype"),

    path('delcomptype/<str:id>',views.delcomptype,name="delcomptype"),
    path('updatecomptype/<str:id>',views.updatecomptype,name="updatecomptype"),

    path('AdminHomepage/',views.adminhomepage,name="adminhomepage"),

    path('Newprofessionals/',views.newprofessionals,name="newprofessionals"),

    path('Approveprofessionals/<str:id>',views.aproveprofessionals,name="aproveprofessionals"),
    path('Rejectprofessionals/<str:id>',views.rejectprofessionals,name="rejectprofessionals"),

    path('Approvedprofessionals/',views.aprovedprofessionals,name="aprovedprofessionals"),
    path('Rejectedprofessionals/',views.rejectedprofessionals,name="rejectedprofessionals"),

    path('Newuser/',views.newuser,name="newuser"),

    path('Complaints/',views.complaints,name="complaints"),
    path('Repliedcomplaint/',views.repliedcomplaint,name="repliedcomplaint"),
    path('eplycomplaints/<str:id>',views.replycomplaints,name="replycomplaints"),
    
    path('Feedback/',views.feedback,name="feedback"),
    path('delpost/<str:id>',views.delpost,name="delpost"),

]
