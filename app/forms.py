from django import forms
from .models import *

#form for the post with widgets
class PostForm(forms.ModelForm):

    class Meta():
        model = Post
        fields = ('author', 'title', 'text')

        widgets = {
            'title': forms.TextInput(attrs= {'class': 'textinputclass'}),
            'text': forms.Textarea(attrs= {'class': 'editable medium-editor-textarea postcontent'})
        }

#comment form with widgets
class CommentForm(forms.ModelForm):

    class Meta():
        model = Comment
        fields = ('author', 'text')

        widgets = {
            'author': forms.TextInput(attrs= {'class': 'textinputclass'}),
            'text': forms.Textarea(attrs= {'class': 'editable medium-editor-textarea postcontent'})
        }
