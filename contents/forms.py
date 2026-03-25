from django import forms

from categories.models import Category
from tags.models import Tag

from .models import CONTENT_TYPE_CHOICES, STATUS_CHOICES, Content

INPUT_CLASS = (
    'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 '
    'text-white placeholder-gray-500 focus:outline-none focus:border-violet-500 '
    'focus:ring-1 focus:ring-violet-500'
)
SELECT_CLASS = (
    'w-full bg-gray-800 border border-gray-700 rounded-lg px-4 py-3 '
    'text-white focus:outline-none focus:border-violet-500 '
    'focus:ring-1 focus:ring-violet-500'
)


class ContentForm(forms.ModelForm):
    class Meta:
        model = Content
        fields = [
            'title', 'url', 'content_type', 'description',
            'category', 'tags', 'status', 'file',
        ]
        widgets = {
            'title': forms.TextInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'Content title',
            }),
            'url': forms.URLInput(attrs={
                'class': INPUT_CLASS,
                'placeholder': 'https://',
            }),
            'content_type': forms.Select(attrs={'class': SELECT_CLASS}),
            'description': forms.Textarea(attrs={
                'class': INPUT_CLASS,
                'rows': 4,
                'placeholder': 'Brief description...',
            }),
            'category': forms.Select(attrs={'class': SELECT_CLASS}),
            'tags': forms.CheckboxSelectMultiple(),
            'status': forms.Select(attrs={'class': SELECT_CLASS}),
            'file': forms.ClearableFileInput(attrs={
                'class': (
                    'w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 '
                    'file:rounded-lg file:border-0 file:text-sm file:font-medium '
                    'file:bg-violet-600/10 file:text-violet-400 '
                    'hover:file:bg-violet-600/20 bg-gray-800 border border-gray-700 '
                    'rounded-lg px-3 py-2'
                ),
                'accept': '.pdf,.jpg,.jpeg,.png,.gif,.webp,.mp3,.mp4,.doc,.docx,.txt,.md',
            }),
        }

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
            self.fields['category'].empty_label = 'No category'
            self.fields['tags'].queryset = Tag.objects.filter(user=user)
        else:
            self.fields['category'].queryset = Category.objects.none()
            self.fields['tags'].queryset = Tag.objects.none()


class ContentFilterForm(forms.Form):
    search = forms.CharField(
        required=False,
        widget=forms.TextInput(attrs={
            'class': INPUT_CLASS,
            'placeholder': 'Search contents...',
        }),
    )
    status = forms.ChoiceField(
        required=False,
        choices=[('', 'All statuses')] + STATUS_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    content_type = forms.ChoiceField(
        required=False,
        choices=[('', 'All types')] + CONTENT_TYPE_CHOICES,
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )
    category = forms.ModelChoiceField(
        required=False,
        queryset=Category.objects.none(),
        empty_label='All categories',
        widget=forms.Select(attrs={'class': SELECT_CLASS}),
    )

    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        if user:
            self.fields['category'].queryset = Category.objects.filter(user=user)
