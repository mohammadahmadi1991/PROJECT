from django import forms
from .models import *

class BlogForm(forms.ModelForm):
    class Meta:
        model=Blog
        fields=['blog_title','blog_text','main_img',]
               
        widgets={
            'blog_title':forms.TextInput(attrs={'placeholder':'Title'}),
            'blog_text':forms.Textarea(attrs={'rows':4,'cols':40,'placeholder':'Text'}),
            # 'main_img':forms.TextInput(attrs={'placeholder':'Image Url'})
        }