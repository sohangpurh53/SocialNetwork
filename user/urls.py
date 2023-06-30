from django.contrib import admin
from django.urls import path, include
from user import views



# Main URl
urlpatterns = [
    # path('Signup', views.Signup, name='Signup'),
    # path('profile/<int:id>', views.profile, name='profile')
    path('create-post/', views.create_post, name='create_post'),
    path('post/<int:post_id>/', views.post_detail, name='post_detail'),
    path('post/<int:post_id>/add-comment/', views.add_comment, name='add_comment'),
    path('post/<int:post_id>/like/', views.like_post, name='like_post'),
    path('follow/<str:username>/', views.follow_user, name='follow_user'),
    path('unfollow/<str:username>/', views.unfollow_user, name='unfollow_user'),
    path('', views.home, name='home'),
    path('profile/<str:username>/', views.profile, name='profile'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('followers/', views.follower_list, name='follower_list'),
    path('messages/', views.message_list, name='message_list'),
    path('messages/conversation/<int:receiver_id>/', views.conversation, name='conversation'),
    path('messages/send/<int:receiver_id>/', views.send_message, name='send_message'),
    path('users/', views.user_list, name='user_list'),
    path('follow/request/<str:username>/', views.follow_request, name='follow_request'),
  path('follow/accept/<str:requester_username>/', views.accept_follow_request, name='accept_follow_request'),
path('follow/reject/<str:requester_username>/', views.reject_follow_request, name='reject_follow_request'),
  path('search/', views.search_results, name='search_results'),
  path('follower/<str:username>/', views.follow_list, name='follow_list'),
    path('following/<str:username>/', views.following_list, name='following_list'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    
]
