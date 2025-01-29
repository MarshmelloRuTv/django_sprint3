from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone

from .models import Post, Category


MAX_COUNT_POST = 5


def filter_posts():
    return Post.objects.filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    )


def index(request):
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    )[:MAX_COUNT_POST]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(filter_posts(), pk=id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    post_list = get_list_or_404(
        filter_posts(),
        category__slug=category_slug
    )
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, 'blog/category.html', context)
