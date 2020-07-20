from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect

# Create your views here.
from Posts.forms import AddPostForm
from Posts.models import Post
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
        form = AddPostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:posts_list')
    else:
        form = AddPostForm()
    return render(request, 'posts/add_post.html', {'form': form})

def post_detail(request, post_id):
    post = Post.objects.get(pk=post_id)
    return render(request, 'posts/post_detail.html', {'post': post})

def edit_post(request, post_id):
    post = Post.objects.get(pk=post_id)

    if request.method == 'POST':
        post.text = request.POST.get('post_text')
        post.save()
        return redirect('posts:posts_list')
    else:
        return render(request, 'posts/edit_post.html', {'post': post})

def delete(request, post_id):
    post = Post.objects.get(pk=post_id)
    post.delete()
    return redirect('/')

