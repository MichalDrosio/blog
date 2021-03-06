from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db import IntegrityError
from django.http import HttpResponseRedirect, Http404
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

@login_required
def add_post(request):
    if request.method == 'POST':
        data = request.POST
        form = AddPostForm(data, request.FILES)
        if form.is_valid():
            new_post = form.save(commit=False)
            try:
                new_post.user = request.user
                new_post.save()
            except ValueError:
                new_post.save()
            return redirect('posts:posts_list')
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', {'form': form})


def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    comments = Comment.objects.filter(post_id=post)
    data = request.POST

    try:
        vote = int(request.POST.get('vote'))
        if vote == 1 or vote == -1:
            post.vote += vote
            post.save()
    except TypeError:
        pass
    except IntegrityError:
        pass

    paginator = Paginator(comments, 3)
    page = request.GET.get('page', 1)
    try:
        comments = paginator.page(page)
    except PageNotAnInteger:
        comments= paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)
    if request.method == 'POST':
        form = CommentForm(data, request.FILES)
        if form.is_valid():
            new_comment = form.save(commit=False)
            new_comment.post = post
            try:
                new_comment.user = request.user
                new_comment.save()
            except ValueError:
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
    posts = Post.objects.filter(user=request.user)
    post = posts.get(pk=post_id)
    if request.method == 'POST':
        post.text = request.POST.get('post_text')
        post.image = request.POST.get('post_image')
        post.save()
        return redirect('posts:post_detail', post_id)
    else:
        return render(request, 'posts/edit_post.html', {'post': post})


@login_required
def delete(request, post_id):
    posts = Post.objects.filter(user=request.user)
    post = posts.get(pk=post_id)
    post.delete()
    return redirect('/')


@login_required
def user_posts_and_comment(request):
    owner_posts = Post.objects.filter(user=request.user).order_by('-created')
    owner_comments = Comment.objects.filter(user=request.user).order_by('-created')
    return render(request, 'posts/owner_posts.html', {'owner_posts': owner_posts, 'owner_comments': owner_comments})


@login_required
def comment_edit(request, comment_id):
    comments = Comment.objects.filter(user=request.user)
    comment = comments.get(pk=comment_id)
    if request.method == 'POST':
        comment.text = request.POST.get('comment_text')
        comment.save()
        return redirect('posts:post_detail', comment.post.id)
    else:
        return render(request, 'posts/edit_comment.html', {'comment': comment})


@login_required
def delete_comment(request, post_id, comment_id):
    comments = Comment.objects.filter(user=request.user)
    comment = comments.get(pk=comment_id)
    comment.delete()
    return redirect('posts:post_detail', post_id)


