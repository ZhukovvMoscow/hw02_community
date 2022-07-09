from django.shortcuts import render, get_object_or_404
from .models import Post, Group
from django.conf import settings


def index(request):
    posts = Post.objects.all().select_related('group',
                                              'author')[:settings.CONSTANT]
    # posts = Post.objects.order_by('-pub_date')[:posti]
    context = {
        'posts': posts,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.filter(group=group).select_related(
        'group', 'author')[:settings.CONSTANT]
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, 'posts/group_list.html', context)
