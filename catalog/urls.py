from django.urls import path
from .views import ProductListView, ContactView, ProductDetailView, ProductCreateView, ProductUpdateView, \
    ProductDeleteView, UnpublishProduct, ProductListByCategoryView

app_name = 'catalog'

urlpatterns = [
    path('', ProductListView.as_view(), name='home'),
    path('contacts/', ContactView.as_view(), name='contacts'),
    path('details/<int:pk>/', ProductDetailView.as_view(), name='details'),
    path('new/', ProductCreateView.as_view(), name='new_product'),
    path('details/update/<int:pk>/', ProductUpdateView.as_view(), name='update_product'),
    path('details/delete/<int:pk>/', ProductDeleteView.as_view(), name='delete_product'),
    path('unpublish/<int:pk>/', UnpublishProduct.as_view(), name='unpublish'),
    path('category/<str:category_name>/', ProductListByCategoryView.as_view(), name='products_by_category'),
]