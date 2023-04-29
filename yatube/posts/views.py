from django.shortcuts import get_object_or_404, render, redirect
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required

from .models import Group, Post, User, Follow, Preferences
from .forms import PostForm, CommentForm

NUMBER_OF_RECORDS_DISPLAYED = 10


def index(request):
    posts = Post.objects.order_by('-pub_date')
    paginator = Paginator(posts, NUMBER_OF_RECORDS_DISPLAYED)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = Post.objects.count()
    context = {
        'posts': posts,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/index.html', context)


@login_required
def index_preference(request):
    prf_group = Preferences.objects.filter(group=request.user)
    prf_group_posts = Post.objects.filter(prf_group).order_by('-pub_date')
    prf_paginator = Paginator(prf_group_posts, NUMBER_OF_RECORDS_DISPLAYED)
    page_number = request.GET.get('page')
    page_obj = prf_paginator.get_page(page_number)
    post_count = Post.objects.count()
    context = {
        'prf_group_posts': prf_group_posts,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/index.html', context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.order_by('-pub_date')
    post_count = group.posts.count()
    paginator = Paginator(posts, NUMBER_OF_RECORDS_DISPLAYED)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'group': group,
        'posts': posts,
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/group_list.html', context)


def profile(request, username):
    author = get_object_or_404(User, username=username)
    posts_list = author.posts.order_by('-pub_date')
    paginator = Paginator(posts_list, NUMBER_OF_RECORDS_DISPLAYED)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = posts_list.count()
    following = (request.user.is_authenticated
                 and author.following.filter(user=request.user).exists())
    context = {
        'author': author,
        'username': username,
        'page_obj': page_obj,
        'post_count': post_count,
        'following': following,
    }
    return render(request, 'posts/profile.html', context)


def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    post_count = post.author.posts.count()
    form = CommentForm()
    comments = post.comments.all()
    context = {
        'post': post,
        'post_count': post_count,
        'form': form,
        'comments': comments,
    }
    return render(request, 'posts/post_detail.html', context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    is_edit = True
    if request.user.id != post.author.id:
        return redirect('posts:post_detail', post_id)
    form = PostForm(request.POST or None, files=request.FILES or None,
                    instance=post)
    if form.is_valid():
        form.save()
        return redirect('posts:post_detail', post_id=post.id)
    return render(request, 'posts/post_create.html',
                  {'form': form, 'is_edit': is_edit})


@login_required
def post_create(request):
    form = PostForm(request.POST or None, files=request.FILES or None)
    if form.is_valid():
        post = form.save(commit=False)
        post.author = request.user
        post.save()
        return redirect('posts:profile', username=request.user.username)
    return render(request, 'posts/post_create.html', {'form': form})


@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    form = CommentForm(request.POST or None)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.author = request.user
        comment.post = post
        comment.save()
    return redirect('posts:post_detail', post_id=post_id)


@login_required
def follow_index(request):
    posts = (Post.objects.filter(author__following__user=request.user).
             order_by('-pub_date'))
    paginator = Paginator(posts, NUMBER_OF_RECORDS_DISPLAYED)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    post_count = posts.count()
    context = {
        'page_obj': page_obj,
        'post_count': post_count,
    }
    return render(request, 'posts/follow.html', context)


@login_required
def profile_follow(request, username):
    author = get_object_or_404(User, username=username)
    if author != request.user:
        Follow.objects.get_or_create(user=request.user, author=author)
    return redirect('posts:profile', author)


@login_required
def profile_unfollow(request, username):
    user_follower = get_object_or_404(
        Follow,
        user=request.user,
        author__username=username
    )
    user_follower.delete()
    return redirect('posts:profile', username)


@login_required
def deletion_post(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    if request.user.id == post.author.id:
        post.delete()
        return render(request, 'posts/deletion_post.html/')
    return redirect('posts:post_detail', post_id=post_id)


def interest(request):
    group_list = Group.objects.all()
    return render(request, 'posts/interests.html', {'group_list': group_list})
