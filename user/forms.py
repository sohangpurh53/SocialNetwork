from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Message, Post

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3}),
        }

class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=100)
    last_name = forms.CharField(max_length=100)
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name',  'password1', 'password2')



    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text = None

class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']

        def __init__(self, *args, **kwargs):
         super().__init__(*args, **kwargs)
         self.fields['content'].help_text = None

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['image', 'caption']