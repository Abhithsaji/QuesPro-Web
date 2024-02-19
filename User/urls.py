from django.urls import path,include
from User import views
app_name = 'webuser'

urlpatterns = [
    path('Userhomepage/',views.homepage,name="homepage"),
    path('Profile/',views.profile,name="profile"),
    path('Editprofile/',views.editprofile,name="editprofile"),
    path('Changepassword/',views.changepassword,name="changepassword"),
    path('Complaints/',views.complaints,name="complaints"),
    path('Feedback/',views.feedback,name="feedback"),
    path('Searchprofessionals/',views.searchprofessionals,name="searchprofessionals"),
    path('ajaxprofession/',views.ajaxprofession,name="ajaxprofession"),
    path('Sendrequest/<str:id>',views.sendrequest,name="sendrequest"),
    path('Following/',views.following,name="following"),
    path('Sendappoinment/<str:id>',views.sendappoinment,name="sendappoinment"),
    path('Professionalprofile/<str:id>',views.professionalprofile,name="professionalprofile"),
    path('Viewappoinment/',views.viewappoinment,name="viewappoinment"),
    # path('Viewcomplaints/',views.viewcomplaints,name="viewcomplaints"),

]
