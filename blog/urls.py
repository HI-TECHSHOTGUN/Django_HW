from django.urls import path
from .views import BlogListView, BlogDetailView, BlogCreateView, BlogUpdateView, BlogDeleteView

app_name = 'blog'

urlpatterns = [
    path('', BlogListView.as_view(), name='blog_list'),
    path('<int:pk>/', BlogDetailView.as_view(), name='blog_details'),
    path('new/', BlogCreateView.as_view(), name='new_post'),
    path('update/<int:pk>/', BlogUpdateView.as_view(), name='update_post'),
    path('delete/<int:pk>/', BlogDeleteView.as_view(), name='delete_post'),
]