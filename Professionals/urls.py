from django.urls import path,include
from Professionals import views
app_name = 'webprofessionals'

urlpatterns = [
    path('Homepageprofessional/',views.homepage,name="homepageprofessional"),

    path('Profile/',views.profile,name="profile"),
    path('Editprofile/',views.editprofile,name="editprofile"),
    path('Changepassword/',views.changepassword,name="changepassword"),

    path('Complaints/',views.complaints,name="complaints"),
    path('Feedback/',views.feedback,name="feedback"),

    path('Newrequest/',views.newrequest,name="newrequest"),
    path('Acceptrequest/<str:id>',views.acceptrequest,name="acceptrequest"),
    path('Rejectrequest/<str:id>',views.rejectrequest,name="rejectrequest"),

    path('Acceptedrequest/',views.acceptedrequest,name="acceptedrequest"),
    path('Rejectedrequest/',views.rejectedrequest,name="rejectedrequest"),

    path('Viewappoinments/',views.viewappoinments,name="viewappoinments"),
    path('acceptappoinment/<str:id>',views.acceptappoinment,name="acceptappoinment"),
    path('rejectappoinment/<str:id>',views.rejectappoinment,name="rejectappoinment"),

    path('Post/',views.post,name="post"),

]
