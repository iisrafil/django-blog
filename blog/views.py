from django.contrib import messages
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)

from .forms import postCreateForm
from .models import Post, Category, Site


def home(request):
    site = Site.objects.all().first()
    site.view = site.view + 1
    site.save()

    post = Post.objects.filter(public='True').order_by('-date_posted')
    paginator = Paginator(post, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj
    }
    return render(request, 'blog/home.html', context)


def pending_post(request):
    site = Site.objects.all().first()
    post = Post.objects.filter(public='False').order_by('-date_posted')

    context = {
        'posts': post
    }
    return render(request, 'blog/pending_post.html', context)


# class PostListView(ListView):
#     model = Post
#     template_name = 'blog/home.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'posts'
#     ordering = ['-date_posted']
#     paginate_by = 5


class UserPostListView(ListView):
    model = Post
    template_name = 'blog/user_posts.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'posts'
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')


# class PostDetailView(DetailView):
#     model = Post

def PostDetail(request, pk):
    site = Site.objects.all().first()
    post = get_object_or_404(Post, pk=pk)
    post.view = post.view + 1
    post.save()
    posts = Post.objects.filter(public='True').exclude(pk=pk).order_by('-date_posted')[:5]

    context = {
        'object': post,
        'posts': posts
    }
    return render(request, 'blog/post_detail.html', context)


# class PostCreateView(LoginRequiredMixin, CreateView):
#     model = Post
#     fields = ['title', 'cover_image', 'content']
#
#     def form_valid(self, form):
#         form.instance.cover_image(self.request.FILES, self.request.POST)
#         form.instance.author = self.request.user
#         return super().form_valid(form)
#

class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'category', 'content', 'cover_image']

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


def PostCreateView(request):
    if request.method == 'POST':
        form = postCreateForm(request.POST, request.FILES)
        if form.is_valid():
            blog_form = form.save(commit=False)
            blog_form.author = request.user
            if request.user.is_staff:
                blog_form.public = True
            blog_form.save()
            messages.success(request, f'Your post has been submitted for approval!')
            return redirect('blog-home')

    else:
        form = postCreateForm(instance=request.user)

    context = {
        'form': form,
    }

    return render(request, 'blog/post_form.html', context)


def approve(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.public = True
    post.save()
    return redirect('pending-post')


class CategoryListView(ListView):
    model = Category
    template_name = 'blog/categories.html'  # <app>/<model>_<viewtype>.html
    context_object_name = 'categories'


def category_post(request, pk):
    category = get_object_or_404(Category, pk=pk)
    post = Post.objects.filter(category=category).order_by('-date_posted')
    paginator = Paginator(post, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'category': category,
        'posts': page_obj
    }
    return render(request, 'blog/category_post.html', context)


def about(request):
    return render(request, 'blog/about.html', {'title': 'About'})
