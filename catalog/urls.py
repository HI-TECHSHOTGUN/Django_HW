from django.urls import path
from . import views

app_name = 'catalog'

urlpatterns = [
    path('about/', views.about, name='about'),
    path('contacts/', views.contact, name='contacts')
]