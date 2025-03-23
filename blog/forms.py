from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Comment, BlogPost, Poll, PollChoice, Blogger

class UserRegistrationForm(UserCreationForm):
    USER_TYPES = (
        ('normal', 'Normal User'),
        ('blogger', 'Blogger'),
    )
    
    user_type = forms.ChoiceField(
        choices=USER_TYPES,
        widget=forms.RadioSelect,
        label='Register as'
    )
    
    bio = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 4}),
        required=False,
        help_text='Required only for bloggers. Tell us about yourself!'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type', 'bio']
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        bio = cleaned_data.get('bio')
        
        if user_type == 'blogger' and not bio:
            raise forms.ValidationError({
                'bio': 'Bio is required for blogger registration'
            })
        
        return cleaned_data

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'content']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }

class PollForm(forms.ModelForm):
    class Meta:
        model = Poll
        fields = ['question']
        widgets = {
            'question': forms.TextInput(attrs={'class': 'form-control'}),
        }

class PollChoiceForm(forms.ModelForm):
    class Meta:
        model = PollChoice
        fields = ['choice_text']
        widgets = {
            'choice_text': forms.TextInput(attrs={'class': 'form-control'}),
        }
