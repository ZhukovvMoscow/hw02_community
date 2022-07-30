from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Group, User
from django.conf import settings
from django.core.paginator import Paginator
from .forms import PostForm
from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required


def index(request):
    post_list = Post.objects.all()
    # Если порядок сортировки определен в классе Meta модели,
    # запрос будет выглядить так:
    # post_list = Post.objects.all()
    # Показывать по 10 записей на странице.
    paginator = Paginator(post_list, settings.CHISPOSTS)

    # Из URL извлекаем номер запрошенной страницы - это значение параметра page
    page_number = request.GET.get('page')

    # Получаем набор записей для страницы с запрошенным номером
    page_obj = paginator.get_page(page_number)
    # Отдаем в словаре контекста
    context = {
        'page_obj': page_obj,
    }
    # posts = Post.objects.all().select_related('group',
    #                                           'author')[:settings.CHISPOSTS]
    # context = {
    #     'posts': posts,
    # }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    post_list = group.posts.select_related('group', 'author')
    paginator = Paginator(post_list, settings.CHISPOSTS)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    # posts = group.posts.select_related(
    #     'group', 'author')[:settings.CHISPOSTS]
    context = {
        'group': group,
        'page_obj': page_obj,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    paginator = Paginator(posts, 10)
    pa_nu = request.GET.get('page')
    page_obj = paginator.get_page(pa_nu)
    context = {
        'author': author,
        'page_obj': page_obj,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    posts = get_object_or_404(Post, pk=post_id)

    # Здесь код запроса к модели и создание словаря контекста
    context = {
        'posts': posts,
        'post_id': post_id,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_create(request):
    form = PostForm(
        request.POST or None,
    )
    title = 'Добавить запись'
    context = {
        'form': form,
        'title': title,
    }
    if form.is_valid():
        form = form.save(commit=False)
        form.author = request.user
        form.save()
        return redirect('posts:profile', request.user.username)
    return render(request, 'posts/create_post.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user != post.author:
        return redirect('posts:post_detail', post_id=post_id)
    form = PostForm(
        request.POST or None,
        instance=post,
    )
    title = 'Редактировать запись'
    context = {
        'form': form,
        'is_edit': True,
        'title': title,
    }
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post_id)
    return render(request, 'posts/create_post.html', context)
# def post_create(request):
#     if request.method == 'POST':
#         form = PostForm(request.POST)
#         if form.is_valid():
#             form = form.save(commit=False)
#             form.author = request.user
#             form.seve
#             return redirect('posts:profile', request.user.username)
#         context = {'form': PostForm(), }
#         return render(request, 'posts/create_post.html', context)
