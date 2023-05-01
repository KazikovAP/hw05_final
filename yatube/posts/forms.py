from django import forms
from .models import Post, Comment, Group, Preferences


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('text', 'group', 'image',)
        help_texts = {
            'text': 'Текст нового поста',
            'group': 'Группа, к которой будет относиться пост',
        }

        labels = {
            'text': 'Выведите текст поста',
            'group': 'Выберите группу',
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('text',)
        help_texts = {
            'text': 'Текст комментраия',
        }

        labels = {
            'text': 'Текст комментраия',
        }


class PreferencesForm(forms.ModelForm):
    group = forms.ModelMultipleChoiceField(
        queryset=Group.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
    )

    class Meta:
        model = Preferences
        exclude = ['user', ]
