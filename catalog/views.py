from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse

from catalog.models import Product


# Create your views here.

def home(req):
    products = Product.objects.all()
    context = {'products': products}
    return render(req, 'catalog/home.html', context=context)


def contacts(req):
    return render(req, 'catalog/contacts.html')


def details(req, detail_id):
    product = get_object_or_404(Product, id=detail_id)
    context = {'product': product}
    return render(req, 'catalog/details.html', context=context)

