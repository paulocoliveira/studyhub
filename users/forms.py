from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

from users.models import CustomUser

_INPUT_CLASS = (
    'w-full px-3 py-2.5 bg-gray-800 border border-gray-700 rounded-lg '
    'text-gray-100 text-sm placeholder-gray-500 '
    'focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 '
    'transition-all duration-200'
)
_SELECT_CLASS = (
    'w-full px-3 py-2.5 bg-gray-800 border border-gray-700 rounded-lg '
    'text-gray-100 text-sm '
    'focus:outline-none focus:ring-2 focus:ring-violet-500/50 focus:border-violet-500 '
    'transition-all duration-200'
)


class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'autocomplete': 'email'}),
    )
    first_name = forms.CharField(max_length=150, required=False)
    last_name = forms.CharField(max_length=150, required=False)

    class Meta:
        model = CustomUser
        fields = ('email', 'first_name', 'last_name', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        if commit:
            user.save()
        return user


class EmailAuthenticationForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'autofocus': True}),
    )
    error_messages = {
        'invalid_login': (
            'Please enter a correct email and password. '
            'Note that both fields may be case-sensitive.'
        ),
        'inactive': 'This account is inactive.',
    }


class UserSettingsForm(forms.ModelForm):
    ai_api_key = forms.CharField(
        required=False,
        widget=forms.PasswordInput(attrs={
            'class': _INPUT_CLASS,
            'placeholder': 'sk-ant-... or sk-...',
            'autocomplete': 'off',
        }),
        help_text='Stored in plaintext. Use a dedicated/restricted key.',
    )

    class Meta:
        model = get_user_model()
        fields = ['ai_provider', 'ai_api_key']
        widgets = {
            'ai_provider': forms.Select(attrs={'class': _SELECT_CLASS}),
        }

    def clean_ai_api_key(self):
        """Keep the existing key when the field is submitted blank."""
        value = self.cleaned_data.get('ai_api_key', '').strip()
        if not value and self.instance and self.instance.pk:
            return self.instance.ai_api_key
        return value
