from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User 
from django.db import IntegrityError
from .models import UserProfile,Community, Membership,Chat, CommunityChat
from .forms import ChatForm, UserProfileForm, CommunityForm, CommunityChatForm
from django.contrib.auth.decorators import login_required

def homefunc(request):
    return render(request,'home.html',{})

def loginfunc(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if not username or not password:
            return render(request,'signup.html', {'error': '全てのフィールドを入力してください'})
        user = authenticate(request,username=username,password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request,'login.html',{'context':'not login'})

    return render(request,'login.html',{'context':'get method'})

def profile_create_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('profile_detail')
    else:
        form = UserProfileForm()

    return render(request, 'profile_create.html', {'form': form})

def profile_update_view(request):
    profile = request.user.profile
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile_detail')
    else:
        form = UserProfileForm(instance=profile)

    return render(request, 'profile_update.html', {'form': form})

def profile_detail_view(request):
    profile = request.user.profile
    return render(request, 'profile_detail.html', {'profile': profile})

def usersfunc(request):
    users = User.objects.exclude(id=request.user.id)
    profile = UserProfile.objects.exclude(id=request.user.id)
    # for i in profile:
    #     print(i.bio)
    return render(request,'users.html',{'users':users,'profile':profile})

def signupfunc(request):
        if request.method=='POST':
            username=request.POST['username']
            email = request.POST['email']
            password=request.POST['password']
            if not username or not email or not password:
                return render(request, 'signup.html', {'error': '全てのフィールドを入力してください'})
            if User.objects.filter(email=email).exists():
                return render(request, 'signup.html', {'error': 'このメールアドレスはすでに使用されています'})
            try:
                user = User.objects.create_user(username, email, password)
                login(request, user)
                return redirect('profile_create') #サインアップ後にログインしてプロフィールを作成してもらう
            except IntegrityError:
                return render(request,'signup.html',{'error':'このユーザーはすでに登録されています'})
        else:
            render(request,'signup.html',{})

        return render(request,'signup.html',{})

def logoutfunc(request):
        logout(request)
        return redirect('home')

def chat_view(request, user_id=None):
    users = User.objects.exclude(id=request.user.id)
    receiver = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = ChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.sender = request.user
            chat.receiver = receiver
            chat.save()
            return redirect('chat', user_id=user_id)
    else:
        form = ChatForm()

    messages = Chat.objects.filter(sender=request.user, receiver=receiver) | Chat.objects.filter(sender=receiver, receiver=request.user)
    messages = messages.order_by('created_at')

    return render(request, 'chatpage.html', {'form': form, 'users': users, 'receiver': receiver, 'messages': messages})


@login_required
def create_community(request):
    if request.method == 'POST':
        form = CommunityForm(request.POST)
        if form.is_valid():
            community = form.save(commit=False)
            community.creator = request.user
            community.save()
            Membership.objects.create(user=request.user, community=community)
            return redirect('community_detail', pk=community.pk)
    else:
        form = CommunityForm()
    return render(request, 'create_community.html', {'form': form})

def community_list(request):
    communities = Community.objects.all()
    return render(request, 'community_list.html', {'communities': communities})

def community_detail(request, pk):
    community = get_object_or_404(Community, pk=pk)
    is_member = request.user.is_authenticated and Membership.objects.filter(user=request.user, community=community).exists()
    return render(request, 'community_detail.html', {'community': community, 'is_member': is_member})

@login_required
def join_community(request, pk):
    community = get_object_or_404(Community, pk=pk)
    Membership.objects.get_or_create(user=request.user, community=community)
    return redirect('community_detail', pk=community.pk)

@login_required
def community_chat(request, pk):
    community = get_object_or_404(Community, pk=pk)
    if request.method == 'POST':
        form = CommunityChatForm(request.POST)
        if form.is_valid():
            chat = form.save(commit=False)
            chat.community = community
            chat.sender = request.user
            chat.save()
            return redirect('community_chat', pk=pk)
    else:
        form = CommunityChatForm()

    messages = CommunityChat.objects.filter(community=community)
    return render(request, 'community_chat.html', {'community': community, 'form': form, 'messages': messages})