from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User

from .forms import AuthenticateForm, UserCreateForm, MozanForm
from .models import Post, Image, UserProfile
from .serializers import PostSerializer, ImageSerializer, UserProfileSerializer
from .permissions import IsOwnerOrReadOnly


from rest_framework import generics, permissions
from rest_framework.renderers import UnicodeJSONRenderer, BrowsableAPIRenderer
from rest_framework.authentication import TokenAuthentication


class PostList(generics.ListCreateAPIView):
    renderer_classes = (UnicodeJSONRenderer, BrowsableAPIRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    renderer_classes = (UnicodeJSONRenderer, BrowsableAPIRenderer,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class ImageList(generics.ListCreateAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class ImageDetail(generics.RetrieveUpdateDestroyAPIView):
    model = Image
    serializer_class = ImageSerializer
    permission_classes = [
        permissions.AllowAny
    ]


class PostImageList(generics.ListAPIView):
    model = Image
    serializer_class = ImageSerializer
    def get_queryset(self):
        queryset = super(PostImageList, self).get_queryset()
        return queryset.filter(post__pk=self.kwargs.get('pk'))


class UserProfileList(generics.ListAPIView):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


class UserProfileDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserProfileSerializer


    def pre_save(self, obj):
        """Force author to the current user on save"""
        obj.owner = self.request.user
        return super(PostMixin, self).pre_save(obj)


def public(request, mozan_form=None):
    mozan_form = mozan_form or MozanForm()
    posts = Post.objects.all().order_by('-creation_date')[:100]
    images = []
    for post in posts:
        images.extend(list(Image.objects.filter(post=post).order_by('id')[:1]))
    return render(request,
                  'public.html',
                  {'mozan_form': mozan_form, 'next_url': '/',
                   'posts': posts, 'username': request.user.username, 'images': images,})



from django.http import Http404
def get_latest(user):
    try:
        return user.post_set.order_by('-id')[0]
    except IndexError:
        return ""



def users(request, username="", mozan_form=None):
    if username:
        # Show a profile
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise Http404
        posts = Post.objects.filter(user=user.id)
        images = []
        for post in posts:
            images.extend(list(Image.objects.filter(post=post).order_by('id')[:1]))
  
        return render(request, 'user.html', {'user': user, 'posts': posts, 'images': images, })



def posts(request, post_id="", mozan_form=None):
    if post_id:
        # Show a post
        try:
            post = Post.objects.get(pk=post_id)
            images = Image.objects.filter(post=post)

        except User.DoesNotExist:
            raise Http404
        return render(request, 'post.html', {'post': post, 'images': images})



def index(request, auth_form=None, user_form=None):
    # User is logged in
    if request.user.is_authenticated():
        mozan_form = MozanForm(request.POST, request.FILES)
        user = request.user
        posts_self = Mozan.objects.filter(user=user.id)
        posts_buddies = Mozan.objects.filter(user__userprofile__in=user.profile.follows.all)
        posts = posts_self | posts_buddies
        return render(request,
                      'buddies.html',
                      {'mozan_form': mozan_form, 
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
        mozan_form = MozanForm(data=request.POST)
        next_url = request.POST.get("next_url", "/")
        if mozan_form.is_valid():
            mozan = mozan_form.save(commit=False)
            mozan.user = request.user
            mozan.save()
            return redirect(next_url)
        else:
            return public(request, mozan_form)
    return redirect('/')



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
