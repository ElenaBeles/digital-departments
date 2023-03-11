from django import forms
from django.contrib.auth import get_user_model
from web.models import Article, Tag

User = get_user_model()


class RegistrationForm(forms.ModelForm):
    password2 = forms.CharField(widget=forms.PasswordInput())

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['password'] != cleaned_data['password2']:
            self.add_error("password", "Пароли не совпадают")
        return cleaned_data

    class Meta:
        model = User
        fields = ("email", "username", "password", "password2")


class AuthForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


class ArticleForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)
    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)

    class Meta:
        model = Article
        fields = ('title', "image", 'description', 'tags')

        widgets = {
            'created_at': forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format='%Y-%m-%dT%H:%M'
            ),
        }

class TagForm(forms.ModelForm):
    description = forms.CharField(widget=forms.Textarea)

    def save(self, commit=True):
        self.instance.user = self.initial['user']
        return super().save(commit)
    class Meta:
        model = Tag
        fields = ('title', 'description')
