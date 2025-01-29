from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.utils import timezone
from .models import Post, Category


def index(request):
    post_list = Post.objects.select_related(
        'category'
    ).filter(
        is_published=True,
        category__is_published=True,
        pub_date__lt=timezone.now()
    ).order_by('-pub_date')[:5]
    context = {'post_list': post_list}
    return render(request, 'blog/index.html', context)


def post_detail(request, id):
    post = get_object_or_404(Post.objects.filter(
        pub_date__lt=timezone.now(),
        is_published=True,
        category__is_published=True), pk=id)
    context = {'post': post}
    return render(request, 'blog/detail.html', context)


def category_posts(request, category_slug):
    post_list = get_list_or_404(
        Post.objects.filter(
            is_published=True,
            category__is_published=True,
            category__slug=category_slug,
            pub_date__lt=timezone.now()
        )
    )

    category = get_object_or_404(Category, slug=category_slug)
    context = {
        'post_list': post_list,
        'category': category
    }
    return render(request, 'blog/category.html', context)
