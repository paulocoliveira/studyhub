from django import forms

from .models import Tag


class TagForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def validate_unique(self):
        if self._user is not None:
            self.instance.user = self._user
        super().validate_unique()

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
