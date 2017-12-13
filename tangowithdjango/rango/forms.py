from django.forms import ModelForm
from django import forms

from .models import Category, Page


class CategoryForm(ModelForm):
    name = forms.CharField(max_length=200, help_text='please enter the category name')
    visits = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    likes = forms.IntegerField(widget=forms.HiddenInput(), initial=0)
    slug = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Category
        fields = ('name',)


class PageForm(ModelForm):
    title = forms.CharField(max_length=200, help_text='please enter page title')
    url = forms.URLField(max_length=200, help_text='please enter page url')
    views = forms.IntegerField(widget=forms.HiddenInput(), initial=0)

    class Meta:
        model = Page
        exclude = ('category',)

    def clean(self):
        cleaned_data = self.cleaned_data
        url = cleaned_data.get('url')
        if url and not url.startswith('http://'):
            url = 'http://' + url
            cleaned_data['url'] = url

        return cleaned_data
