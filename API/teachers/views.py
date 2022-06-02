from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect

# Create your views here.
def redirect_login(request):
    return HttpResponseRedirect('/teacher/login/')
