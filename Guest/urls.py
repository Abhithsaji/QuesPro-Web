from django.urls import path,include
from Guest import views
app_name = 'webguest'

urlpatterns = [
    path('Professionalregistration/',views.Professionalregistration,name="Professionalregistration"),
    path('Login/',views.login,name="login"),
    path('Userregistration/',views.userregistration,name="userregistration"),
    path('ajaxplace/',views.ajaxplace,name="ajaxplace"),
    path('Login/',views.login,name="login"),
]