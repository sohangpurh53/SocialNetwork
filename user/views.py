from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import UserProfile, Post, Comment, Like, Follow, Message, FollowRequest
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import UserProfileForm, SignUpForm, MessageForm, EditPostForm
from django.db.models import Max
from django.db.models import Q
from django.http import HttpResponse

@login_required(login_url='signin')
def create_post(request):
    if request.method == 'POST':
        image = request.FILES['image']
        caption = request.POST['caption']
        post = Post(user=request.user, image=image, caption=caption)
        post.save()
        return redirect('home')
    return render(request, 'create_post.html')

@login_required(login_url='signin')
def post_detail(request, post_id):
    post = Post.objects.get(id=post_id)
    comments = Comment.objects.filter(post=post)
    likes = Like.objects.filter(post=post)
    return render(request, 'post_detail.html', {'post': post, 'comments': comments, 'likes': likes})

@login_required(login_url='signin')
def add_comment(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(id=post_id)
        text = request.POST['comment']
        comment = Comment(user=request.user, post=post, text=text)
        comment.save()
    return redirect('post_detail', post_id=post_id)

@login_required(login_url='signin')
def like_post(request, post_id):
    post = Post.objects.get(id=post_id)
    like, created = Like.objects.get_or_create(user=request.user, post=post)
    if not created:
        like.delete()
    return redirect('post_detail', post_id=post_id)

@login_required
def follow_user(request, username):
    follower = request.user
    following = User.objects.get(username=username)

    if follower != following:
        follow_request, created = FollowRequest.objects.get_or_create(
            requester=follower,
            recipient=following
        )


    return redirect('profile', username=username)

@login_required(login_url='signin')
def unfollow_user(request, username):
    follower = request.user
    following = get_object_or_404(User, username=username)

    follow = Follow.objects.filter(follower=follower, following=following).first()
    if follow:
        follow.delete()
    return redirect('profile', username=username)

@login_required(login_url='signin')
def home(request):
    following_users = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    posts = Post.objects.filter(Q(user__in=following_users) | Q(user=request.user)).order_by('-created_at')
    return render(request, 'homepage.html', {'posts': posts})

@login_required(login_url='signin')
def profile(request, username):
    user = User.objects.get(username=username)
    profile = UserProfile.objects.get(user=user)
    posts = Post.objects.filter(user=user).order_by('-created_at')
    followers = Follow.objects.filter(following=user).count()
    following = Follow.objects.filter(follower=user).count()


    if request.user == user:
        follow_status = 'self'
    elif Follow.objects.filter(follower=request.user, following=user).exists():
        follow_status = 'following'
    elif FollowRequest.objects.filter(requester=request.user, recipient=user).exists():
        follow_status = 'requested'
    elif FollowRequest.objects.filter(requester=user, recipient=request.user).exists():
        follow_status = 'pending'
    else:
        follow_status = 'none'

    follow_requests = FollowRequest.objects.filter(recipient=request.user)

    return render(request, 'profile.html', {'user': user, 'profile': profile, 'posts': posts, 'followers': followers, 'following': following, 'follow_status': follow_status, 'follow_requests': follow_requests, })


def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            return redirect('signin')  # Replace 'home' with the desired URL name for the homepage
    else:
        form = SignUpForm()
        
    return render(request, 'signup.html', {'form': form})

def signin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')  # Replace 'home' with the desired URL name for the homepage
    else:
        form = AuthenticationForm()
    return render(request, 'signin.html', {'form': form})

def signout(request):
    logout(request)
    messages.success(request, ('Logout Successfull'))
    return redirect('signin')

@login_required(login_url='signin')
def update_profile(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        user_profile = UserProfile(user=request.user)

    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user_profile)
        if form.is_valid():
            form.save()
            return redirect('profile', username=request.user.username)
    else:
        form = UserProfileForm(instance=user_profile)

    context = {
        'form': form
    }
    return render(request, 'update_profile.html', context)


@login_required(login_url='signin')
def follower_list(request):
     follow_requests = FollowRequest.objects.filter(recipient=request.user)
     return render(request, 'follow_request_list.html', {'follow_requests': follow_requests})

@login_required(login_url='signin')
def message_list(request):
    followers = Follow.objects.filter(follower=request.user).values_list('following', flat=True)
    users = User.objects.filter(id__in=followers).exclude(id=request.user.id)
    return render(request, 'message_list.html', {'users': users})

@login_required(login_url='signin')
def conversation(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    messages = Message.objects.filter(sender=request.user, receiver=receiver) | Message.objects.filter(sender=receiver, receiver=request.user)
    return render(request, 'conversation.html', {'receiver': receiver, 'messages': messages})

@login_required(login_url='signin')
def send_message(request, receiver_id):
    receiver = User.objects.get(id=receiver_id)
    
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message(sender=request.user, receiver=receiver, content=form.cleaned_data['content'])
            message.save()
            return redirect('conversation', receiver_id=receiver_id)
    else:
        form = MessageForm()
    
    return render(request, 'send_message.html', {'form': form, 'receiver': receiver})


@login_required(login_url='signin')
def user_list(request):
    users = User.objects.exclude(id=request.user.id).exclude(followers__follower=request.user)
    return render(request, 'user_list.html', {'users': users})


@login_required(login_url='signin')
def follow_request(request, username):
    follower = request.user
    following = User.objects.get(username=username)

    if follower != following:
        follow, created = Follow.objects.get_or_create(follower=follower, following=following)
        if created:
            follow.status = Follow.FOLLOW_REQUESTED
            follow.save()
            messages.info(request, f"You have sent a follow request to {following.username}")

    return redirect('profile', username=username)

@login_required(login_url='signin')
def accept_follow_request(request, requester_username):
    requester = User.objects.get(username=requester_username)
    follow_request = FollowRequest.objects.filter(requester=requester, recipient=request.user).first()
    if follow_request:
        Follow.objects.create(follower=requester, following=request.user)
        follow_request.delete()
        messages.info(request, f"You have accepted the follow request from {requester.username}")
    return redirect('follower_list')

@login_required(login_url='signin')
def reject_follow_request(request, requester_username):
    requester = User.objects.get(username=requester_username)
    follow_request = FollowRequest.objects.filter(requester=requester, recipient=request.user).first()
    if follow_request:
        follow_request.delete()
        messages.info(request, f"You have rejected the follow request from {requester.username}")
    return redirect('follower_list')




@login_required(login_url='signin')
def search_results(request):
    query = request.GET.get('query', '')
    posts = Post.objects.filter(Q(caption__icontains=query) | Q(user__username__icontains=query))
    users = User.objects.filter(username__icontains=query)
    return render(request, 'search_results.html', {'posts': posts, 'users': users, 'query': query})


@login_required(login_url='signin')
def follow_list(request, username):
    user = User.objects.get(username=username)
    followers = Follow.objects.filter(following=user)
    return render(request, 'follow_list.html', {'user': user, 'followers': followers})

@login_required(login_url='signin')
def following_list(request, username):
    user = User.objects.get(username=username)
    following = Follow.objects.filter(follower=user)
    return render(request, 'following_list.html', {'user': user, 'following': following})

@login_required(login_url='signin')
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the current user is the owner of the post
    if post.user == request.user: 
     if request.method == 'POST':
        post.delete()
        messages.success(request, ('Invoice Deleted Succesfully'))
        return redirect('home')
    context = {
        'post': post
    }
    return render(request, 'delete.html', context)




@login_required(login_url='signin')
def edit_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    # Check if the current user is the owner of the post
    if post.user == request.user:
        if request.method == 'POST':
            # Update the post with the new data
            form = EditPostForm(request.POST, request.FILES, instance=post)
            if form.is_valid():
                form.save()
                return redirect('post_detail', post_id=post_id)
        else:
            form = EditPostForm(instance=post)
        
        return render(request, 'edit_post.html', {'form': form, 'post': post})
    else:
        # Handle the case where the current user is not the owner of the post
        # You can show an error message or redirect to an appropriate page
        return HttpResponse("You are not authorized to edit this post.")
