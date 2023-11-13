from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import Http404

from .models import BlogPost
from .forms import PostForm

@login_required
def index(request):
    posts = BlogPost.objects.filter(owner=request.user).order_by('-date_added')
    # post = BlogPost()
    # if post.owner != request.user:
    #     raise Http404

    context = {'posts': posts}
    return render(request, 'index.html', context)

@login_required
def new_post(request):

    if request.method != 'POST':
        form = PostForm()
    else:
        form = PostForm(data=request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            form.save()
            return redirect('blogs:index')

    # Вывести пустую или недействительную форму
    context = {'form': form}
    return render(request, 'new_post.html', context)

@login_required
def edit_post(request, post_id):

    post = BlogPost.objects.get(id=post_id)
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        form = PostForm(instance=post)
    else:
        form = PostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('blogs:index')

    # Вывести пустую или недействительную форму
    context = {'form': form, 'post': post}
    return render(request, 'edit_post.html', context)
