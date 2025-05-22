from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def about(req):
    return render(req, 'students/about.html')


def contact(req):
    if req.method == 'POST':
        name = req.POST.get('name')
        message = req.POST.get('message')

        return HttpResponse(f'Thank you, {name} message finish')
    return render(req, 'students/contact.html')