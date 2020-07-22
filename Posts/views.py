from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from Posts.forms import AddPostForm, CommentForm
from Posts.models import Post, Comment
from django.db.models import Q


def show_all_posts(request):
    search_query = request.GET.get('search', '')
    if search_query:
        posts = Post.objects.filter(Q(name__icontains=search_query) | Q(text__icontains=search_query))
    else:
        posts = Post.objects.all()
    paginator = Paginator(posts, 2)
    page = request.GET.get('page', 1)
    try:
        posts_num = paginator.page(page)
    except PageNotAnInteger:
        posts_num = paginator.page(1)
    except EmptyPage:
        posts_num = paginator.page(paginator.num_pages)
    return render(request, 'posts/list_posts.html', {'posts': posts_num, 'page':page})


def add_post(request):
    if request.method == 'POST':
        form = AddPostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.user = request.user
            new_post.save()
            return redirect('posts:posts_list')
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', {'form': form})


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post)
    paginator = Paginator(comments, 3)
    page = request.GET.get('page', 1)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments= paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = CommentForm(data=request.POST, )
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, 'Dodano komentarz')
        else:
            messages.error(request, 'Wystąpił błąd podczas dodawania komentarza')
        return HttpResponseRedirect(reverse('posts:post_detail', args=[post_id]))
    else:
        form = CommentForm()
    return render(request, 'posts/post_detail.html', {'post': post, 'form': form, 'comments': comments, 'page': page})

@login_required
def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        post.text = request.POST.get('post_text')
        post.save()
        return redirect('posts:post_detail', post_id)
    else:
        return render(request, 'posts/edit_post.html', {'post': post})


def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('/')


def user_posts(request):
    owner_posts = Post.objects.filter(user=request.user).order_by('-created')
    return render(request, 'posts/owner_posts.html', {'owner_posts': owner_posts})



