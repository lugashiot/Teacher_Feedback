from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_page),
    #path('send_mails/', views.send_mails),
]