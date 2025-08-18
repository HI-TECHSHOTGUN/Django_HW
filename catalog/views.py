from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseForbidden, Http404
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.cache import cache

from catalog.forms import ProductForm
from catalog.models import Product, Category
from catalog.services import ProductService


# Create your views here.
class ProductListByCategoryView(ListView):
    model = Product
    template_name = 'catalog/products_by_category.html'
    context_object_name = 'products_category'

    def get_queryset(self):
        category_name = self.kwargs.get('category_name')
        cache_key = f'products_{category_name}'
        queryset = cache.get(cache_key)
        if not queryset:
            queryset = ProductService.get_products_by_category(category_name)
            cache.set(cache_key, list(queryset), 60 * 3)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category_name'] = self.kwargs.get('category_name')
        context['categories'] = Category.objects.all()
        return context


class ProductListView(ListView):
    model = Product
    template_name = "catalog/home.html"
    context_object_name = "products"

    def get_queryset(self):
        queryset = cache.get('products_queryset')
        if not queryset:
            queryset = super().get_queryset()
            cache.set('products_queryset', queryset, 60 * 3)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context


@method_decorator(cache_page(60 * 3), name='dispatch')
class ProductDetailView(LoginRequiredMixin, DetailView):
    model = Product
    template_name = "catalog/details.html"
    context_object_name = "product_detail"



class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy("catalog:home")

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise Http404("Product does not exist")
        product = Product.objects.get(pk=pk)
        if product.owner != self.request.user and not self.request.user.has_perm(
                "catalog.can_unpublish_product"):
            return HttpResponseForbidden("У вас нет прав на редактирование этого продукта.")
        return product


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    template_name = "catalog/product_delete.html"
    success_url = reverse_lazy("catalog:home")

    def get_object(self):
        pk = self.kwargs.get('pk')
        if not pk:
            raise Http404("Product does not exist")
        product = Product.objects.get(pk=pk)
        if product.owner != self.request.user and not self.request.user.has_perm("catalog.delete_any_product"):
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

        product.is_published = False
        product.save()

        return redirect("catalog:details", pk=pk)
