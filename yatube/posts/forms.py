import pymorphy2

from django import forms

from .models import Post, Comment, Group, Preferences

morph = pymorphy2.MorphAnalyzer()


class PostForm(forms.ModelForm):

    def lemmatize(self, text):
        words = text.split()
        result = []
        for word in words:
            p = morph.parse(word)[0]
            result.append(p.normal_form)

        result1 = []
        for x in result:
            if x not in result1:
                result1.append(x)

        return result1

    def clean(self):
        """
        Проверяет, соответствует ли текст поста ключевым словам выбранной группы.
        Если нет, ищет наиболее подходящую группу и устанавливает ее для поста.
        Возвращает обновленные очищенные данные.
        """
        self.errors.clear()
        cleaned_data = super().clean()
        text = cleaned_data.get('text')
        text = self.lemmatize(text)
        group = cleaned_data.get('group')

        if group and not self.group_matches_text(group, text):
            most_matching_group = self.find_most_matching_group(text)
            if most_matching_group:
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
        text = self.lemmatize(text)
        k_words_list = group.k_words.split(',')
        new_kwargs = [k_word.strip() for k_word in k_words_list]
<<<<<<< HEAD
        return bool(list(set(text) & set(new_kwargs)))
=======
        return bool(list(set(text.split()) & set(new_kwargs)))
>>>>>>> a18c8179dd614c20037ce33423cb7c295b1a2741

    def find_most_matching_group(self, text):
        """
        Ищет наиболее подходящую группу на основе количества совпадающих ключевых слов с заданным текстом.
        :param text: текст поста
        :return: экземпляр модели Group с наибольшим количеством совпадающих ключевых слов или None, если нет совпадений
        """
        groups = Group.objects.all()
        group_matches = {}
<<<<<<< HEAD
        text = self.lemmatize(text)

        for group in groups:
            k_words_list = group.k_words.split(',')

=======

        for group in groups:
            k_words_list = group.k_words.split(',')
>>>>>>> a18c8179dd614c20037ce33423cb7c295b1a2741
            new_kwargs = [k_word.strip() for k_word in k_words_list]
            count_kwargs = len(list(set(text.split()) & set(new_kwargs)))
            if count_kwargs:
                group_matches[group] = count_kwargs

        if group_matches:
            most_matching_group = max(group_matches, key=group_matches.get)
            return most_matching_group
        else:
<<<<<<< HEAD
            self.add_error(None, 'Текст поста не соответствует не одной группе. Добавьте пост без группы или в группу "Всякое".')
=======
            self.add_error(None, f'Текст поста не соответствует выбранной группе и подходящая группа не найдена.')
>>>>>>> a18c8179dd614c20037ce33423cb7c295b1a2741

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
