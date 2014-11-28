from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from karma_app.forms import AuthenticateForm, UserCreateForm, KarmaForm
from karma_app.models import Post, Image

def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        karma_form = KarmaForm(request.POST, request.FILES)
        user = request.user
        posts_self = Karma.objects.filter(user=user.id)
        posts_buddies = Karma.objects.filter(user__userprofile__in=user.profile.follows.all)
        posts = posts_self | posts_buddies
 
        return render(request,
                      'buddies.html',
                      {'karma_form': karma_form, 
                       'user': user,
                       'posts': posts,
                       'next_url': '/',})
    else:
        # User is not logged in
        auth_form = auth_form or AuthenticateForm()
        user_form = user_form or UserCreateForm()
 
        return render(request,
                      'home.html',
                      {'auth_form': auth_form, 
                       'user_form': user_form, })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticateForm(data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            # Success
            return redirect('/')
        else:
            # Failure
            return index(request, auth_form=form)
    return redirect('/')

def logout_view(request):
    logout(request)
    return redirect('/')

def signup(request):
    user_form = UserCreateForm(data=request.POST)
    if request.method == 'POST':
        if user_form.is_valid():
            username = user_form.clean_username()
            password = user_form.clean_password2()
            user_form.save()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('/')
        else:
            return index(request, user_form=user_form)
    return redirect('/')

from django.contrib.auth.decorators import login_required
 
@login_required
def submit(request):
    if request.method == "POST":
        karma_form = KarmaForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if karma_form.is_valid():
            karma = karma_form.save(commit=False)
            karma.user = request.user
            karma.save()
            return redirect(next_url)
        else:
            return public(request, karma_form)
    return redirect('/')

def public(request, karma_form=None):
    karma_form = karma_form or KarmaForm()
    posts = Post.objects.all().order_by('-creation_date')[:100]
    images = Image.objects.all().order_by('-id')
    return render(request,
                  'public.html',
                  {'karma_form': karma_form, 'next_url': '/',
                   'posts': posts, 'username': request.user.username, 'images': images,})



from django.db.models import Count
from django.http import Http404
 
def get_latest(user):
    try:
        return user.post_set.order_by('-id')[0]
    except IndexError:
        return ""
 
 

def users(request, username="", karma_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        posts = Post.objects.filter(user=user.id)
        return render(request, 'user.html', {'user': user, 'posts': posts, })

def posts(request, post_id="", karma_form=None):
    if post_id:
        # Show a post
        try:
            post = Post.objects.get(pk=post_id)
            images = Image.objects.filter(post=post)
        except User.DoesNotExist:
            raise Http404
        return render(request, 'post.html', {'post': post, 'images': images})



from django.core.exceptions import ObjectDoesNotExist
 
@login_required
def follow(request):
    if request.method == "POST":
        follow_id = request.POST.get('follow', False)
        if follow_id:
            try:
                user = User.objects.get(id=follow_id)
                request.user.profile.follows.add(user.profile)
            except ObjectDoesNotExist:
                return redirect('/users/')
    return redirect('/users/')
