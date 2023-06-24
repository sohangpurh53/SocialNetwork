from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return self.user.username
    


class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='posts/')
    caption = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s post"


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s comment on {self.post.caption}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.username} liked {self.post.caption}"


class Follow(models.Model):
    FOLLOW_REQUESTED = 'requested'
    FOLLOW_ACCEPTED = 'accepted'
    FOLLOW_REJECTED = 'rejected'

    FOLLOW_STATUS_CHOICES = (
        (FOLLOW_REQUESTED, 'Requested'),
        (FOLLOW_ACCEPTED, 'Accepted'),
        (FOLLOW_REJECTED, 'Rejected'),
    )

    follower = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE)
    following = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=FOLLOW_STATUS_CHOICES, default=FOLLOW_ACCEPTED)

    def __str__(self):
        return f"{self.follower.username} follows {self.following.username} ({self.get_status_display()})"

class FollowRequest(models.Model):
    requester = models.ForeignKey(User, related_name='follow_requests_sent', on_delete=models.CASCADE)
    recipient = models.ForeignKey(User, related_name='follow_requests_received', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.requester.username} sent follow request to {self.recipient.username}"


class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}"

