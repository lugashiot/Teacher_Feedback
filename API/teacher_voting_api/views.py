from django.shortcuts import render, redirect
from django.http import HttpResponse


def main_page(request):
    return render(request, 'main_page.html')
