from django import forms

from .models import Category


class CategoryForm(forms.ModelForm):
    def __init__(self, *args, user=None, **kwargs):
        super().__init__(*args, **kwargs)
        self._user = user

    def validate_unique(self):
        # user is injected here so unique_together ['name', 'user'] validates
        # correctly at form validation time, before form_valid sets the instance user.
        if self._user is not None:
            self.instance.user = self._user
        super().validate_unique()

    class Meta:
        model = Category
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': (
                    'w-full bg-gray-800 border border-gray-700 rounded-lg '
                    'px-4 py-3 text-white placeholder-gray-500 '
                    'focus:outline-none focus:border-violet-500 '
                    'focus:ring-1 focus:ring-violet-500'
                ),
            }),
            'description': forms.Textarea(attrs={
                'class': (
                    'w-full bg-gray-800 border border-gray-700 rounded-lg '
                    'px-4 py-3 text-white placeholder-gray-500 '
                    'focus:outline-none focus:border-violet-500 '
                    'focus:ring-1 focus:ring-violet-500'
                ),
                'rows': 3,
            }),
        }
