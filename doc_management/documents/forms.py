from django import forms
from .models import Document, Post, Comment


class DocumentForm(forms.ModelForm):
    class Meta:
        model = Document
        fields = ["title", "description", "file"]  # descriptionフィールドを追加


class DocumentSearchForm(forms.Form):
    query = forms.CharField(label="検索", max_length=100, required=False)


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ["title", "content"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control"}),
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(
                attrs={"rows": 2, "class": "form-control", "placeholder": "返信を書く…"}
            ),
        }
