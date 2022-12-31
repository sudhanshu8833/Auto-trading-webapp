from django.shortcuts import render
from django.http import HttpResponse

def home(request):
    return render(request,"shop/home.html")

def about(request):
    return render(request,"shop/about.html")

def contact(request):
    return render(request,"shop/contact.html")
