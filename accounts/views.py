from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from Posts.models import Post
from accounts.forms import LoginForm, UserRegistrationForm, UserEditForm


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request,
                                email=cd['username'],
                                password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    messages.success(request, 'Zalogowano')
                    return redirect('posts:posts_list')
            else:
                messages.error(request, 'Nieprawidłowe dane')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})

def register_user(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            new_user.set_password(form.cleaned_data['password'])
            new_user.save()
            return render(request, 'posts/list_posts.html', {'new_user': new_user})
    else:
        form = UserRegistrationForm()
    return render(request, 'account/register.html', {'form': form})

def user_logout(request):
    logout(request)
    return render(request, 'posts/list_posts.html')

def edit_user(request):
    if request.method == "POST":
        form = UserEditForm(data=request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Aktualizacja wykonan')
            return redirect('posts:posts_list')
        else:
            messages.error(request, 'Nie udało się zaktualizować danych')
    else:
        form = UserEditForm(instance=request.user)
    return render(request, 'account/owner.html', {'form': form})


