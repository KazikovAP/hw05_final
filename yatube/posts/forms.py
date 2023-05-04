from collections import Counter

from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Comment, Group, Preferences


class PostForm(forms.ModelForm):
    def clean(self):
        """
        Проверяет, соответствует ли текст поста ключевым словам выбранной группы.
        Если нет, ищет наиболее подходящую группу и устанавливает ее для поста.
        Возвращает обновленные очищенные данные.
        """
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        group = cleaned_data.get('group')

        if group and not self.group_matches_text(group, text):
            most_matching_group = self.find_most_matching_group(text)
            cleaned_data['group'] = most_matching_group
            self.add_error(None, f'Текст поста не соответствует выбранной группе. '
                                 f'Была выбрана наиболее подходящая группа "{most_matching_group}"')

        return cleaned_data

    def group_matches_text(self, group, text):
        """
        Проверяет, содержит ли текст поста хотя бы одно ключевое слово из заданной группы.

        :param group: экземпляр модели Group
        :param text: текст поста
        :return: True, если текст содержит хотя бы одно ключевое слово из группы, иначе False
        """
        k_words_list = group.k_words.split(',')
        return any(k_word.strip() in text for k_word in k_words_list)

    def find_most_matching_group(self, text):
        """
        Ищет наиболее подходящую группу на основе количества совпадающих ключевых слов с заданным текстом.

        :param text: текст поста
        :return: экземпляр модели Group с наибольшим количеством совпадающих ключевых слов или None, если нет совпадений
        """
        groups = Group.objects.all()
        group_matches = Counter()

        for group in groups:
            k_words_list = group.k_words.split(',')

            for k_word in k_words_list:
                if k_word.strip() in text:
                    group_matches[group] += 1

        if group_matches:
            most_matching_group, _ = group_matches.most_common(1)[0]
            return most_matching_group
        else:
            raise ValidationError('Текст поста не соответствует выбранной группе и подходящая группа не найдена.')

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
            'text': 'Текст комментария',
        }

        labels = {
            'text': 'Текст комментария',
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
