from django import forms

from .models import Tag


class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': (
                    'w-full bg-gray-800 border border-gray-700 rounded-lg '
                    'px-4 py-3 text-white placeholder-gray-500 '
                    'focus:outline-none focus:border-violet-500 '
                    'focus:ring-1 focus:ring-violet-500'
                ),
            }),
        }
