from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect


def main_page(request):
    return render(request, 'main_page.html')

def redirect_login(request):
    return HttpResponseRedirect('/teacher/login/')