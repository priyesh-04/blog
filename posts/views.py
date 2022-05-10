from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.views.generic.edit import DeleteView
from .models import Post
from .forms import PostForm
    

class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"


class PostCreateView(CreateView):
    form_class = PostForm
    template_name = "posts/post_create.html"

class PostUpdateView(UpdateView):
    model = Post
    fields = '__all__'
    template_name = "posts/post_update.html"


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = reverse_lazy('post:list-view')