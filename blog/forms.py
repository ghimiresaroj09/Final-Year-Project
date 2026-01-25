from django import forms
from .models import BlogComment

class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['author_name', 'author_email', 'content']
        widgets = {
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Name'
            }),
            'author_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Email'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Your Comment',
                'rows': 4
            }),
        }
