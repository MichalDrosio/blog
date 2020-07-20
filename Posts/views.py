from django.shortcuts import render, redirect

# Create your views here.
from Posts.forms import AddPostForm
from Posts.models import Post


def show_all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/list_posts.html', {'posts': posts})

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

def delete(request):
    post_id = request.POST.get('id')
    post = Post.objects.get(pk=post_id)
    if request.method == 'POST':
        post.delete()
    posts = Post.objects.all()
    return render(request, 'posts/list_posts.html', context={'posts':posts})


