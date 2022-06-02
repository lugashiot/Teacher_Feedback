from django.urls import path
from . import views

urlpatterns = [
    path('', views.feedback_page),
    path('uuid_used/', views.uuid_used_page),
    path('success/', views.success_page),
    path('send_mails/', views.send_mails),
]