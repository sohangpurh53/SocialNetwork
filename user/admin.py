from django.contrib import admin
from .models import UserProfile, Post, Comment, Like, Follow, Message, FollowRequest
# Register your models here.
admin.site.register(UserProfile)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Like)
admin.site.register(Follow)
admin.site.register(Message)
admin.site.register(FollowRequest)