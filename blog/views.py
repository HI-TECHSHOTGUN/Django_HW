from django.shortcuts import render

# Create your views here.


from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from .models import BlogPost

class PostListView(ListView):
    model = BlogPost
    template_name = 'blog/blog_home.html'
    queryset = BlogPost.objects.filter(is_published=True)
    context_object_name = 'blog_home'

class PostDetailView(DetailView):
    model = BlogPost
    template_name = 'blog/blog_detail.html'
    context_object_name = 'blog_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=None)
        obj.views += 1
        obj.save()
        return obj

class PostCreateView(CreateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'  # Создайте этот шаблон
    fields = ['name', 'description', 'photo', 'is_published']

class PostUpdateView(UpdateView):
    model = BlogPost
    template_name = 'blog/blog_form.html'  # Создайте этот шаблон
    fields = ['name', 'description', 'photo', 'is_published']
    success_url = reverse_lazy('blog_home') # Перенаправление после редактирования

class PostDeleteView(DeleteView):
    model = BlogPost
    template_name = 'blog/blog_confirm_delete.html'  # Создайте этот шаблон
    success_url = reverse_lazy('blog_home')

