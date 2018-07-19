from django import forms
from django.contrib.auth.models import User
from . models import Page, Category, UserProfile


class Style:
    def __init__(self, x):
        self.tags = x

    def inputs(self):
        for i in self.tags:
            htmlclass = {'class': 'form-control-sm', 'placeholder': i[1]}
            i[0].widget.attrs.update(htmlclass)


class UserForm(forms.ModelForm):
    username = forms.CharField()
    email = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    style = Style([[username, 'Username'], [email, 'Email'], [password, 'Password']])
    style.inputs()

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileForm(forms.ModelForm):
    website = forms.URLField(required=False)
    picture = forms.FileField(help_text='Picture:', required=False)
    style = Style([[website, 'Website'], [picture, None]])
    style.inputs()


    class Meta:
        model = UserProfile
        fields = ('website', 'picture')


class CategoryForm(forms.ModelForm):
    name = forms.CharField(max_length=128)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    style = Style([[name, 'Add New Category']])
    style.inputs()

    class Meta:
        model = Category
        fields = ('name', 'likes', 'views')


class PageForm(forms.ModelForm):
    title = forms.CharField(max_length=128, help_text="Please Enter Page Title")
    url = forms.URLField(max_length=250, help_text="Please Enter Page URL")
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    style = Style([[title, 'Title'], [url, 'URL']])
    style.inputs()

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')

        if url and not url.startswith('http://'):
            url = 'http://' + str(url)
            cleaned_data['url'] = url

        return cleaned_data

    class Meta:
        model = Page
        fields = ('title', 'url', 'views')
