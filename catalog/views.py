from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from catalog.forms import ProductForm
from catalog.models import Product


# Create your views here.


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/home.html'
    context_object_name = 'products'


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = 'catalog/details.html'
    context_object_name = 'product_detail'

class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')



class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:home')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_delete.html'
    success_url = reverse_lazy('catalog:home')


class ContactView(LoginRequiredMixin, TemplateView):
    model = Product
    template_name = 'catalog/contacts.html'


class UnpublishProduct(LoginRequiredMixin, View):
    def post(self, req, pk):
        product = get_object_or_404(Product, id=pk)

        if not req.user.has_perm('catalog.can_unpublish_product'):
            return HttpResponseForbidden('У вас нет нужных прав, для продолжения нужно иметь права уровня МОДЕРАТОР')

        product.is_published = True
        product.save()

        return redirect('catalog:details', pk=pk)
