from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
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
    template_name = "catalog/home.html"
    context_object_name = "products"


class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/details.html"
    context_object_name = "product_detail"

    def get_object(self):
        obj = super().get_object()
        if obj.owner != self.request.user:
            return HttpResponseForbidden("У вас нет прав на просмотр этого продукта.")
        return obj


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise Http404("Product does not exist")
        product = Product.objects.get(pk=pk)
        if product.owner != self.request.user:
            return HttpResponseForbidden("У вас нет прав на удаление этого продукта.")
        return product


class ContactView(LoginRequiredMixin, TemplateView):
    model = Product
    template_name = "catalog/contacts.html"


class UnpublishProduct(LoginRequiredMixin, View):
    def post(self, req, pk):
        product = get_object_or_404(Product, id=pk)

        if not req.user.has_perm("catalog.can_unpublish_product"):
            return HttpResponseForbidden(
                "У вас нет нужных прав, для продолжения нужно иметь права уровня МОДЕРАТОР"
            )

        product.is_published = True
        product.save()

        return redirect("catalog:details", pk=pk)
