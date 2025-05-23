from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def home(req):
    return render(req, 'catalog/home.html')


def contact(req):
    return render(req, 'catalog/contacts.html')