from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from users.models import User

from team_finder.mixins import GitHubUrlMixin


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['name', 'surname', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class LoginForm(forms.Form):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)


class EditProfileForm(GitHubUrlMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'surname', 'avatar', 'about', 'phone', 'github_url']

    def __init__(self, *args, **kwargs):
        self.current_user = kwargs.pop('current_user', None)
        super().__init__(*args, **kwargs)

    def clean_phone(self):
        import re
        phone = self.cleaned_data.get('phone', '')
        if not phone:
            return phone
        if re.match(r'^8\d{10}$', phone):
            phone = '+7' + phone[1:]
        if not re.match(r'^\+7\d{10}$', phone):
            raise forms.ValidationError(
                'Введите номер в формате 8XXXXXXXXXX или +7XXXXXXXXXX'
            )
        qs = User.objects.filter(phone=phone)
        if self.current_user:
            qs = qs.exclude(pk=self.current_user.pk)
        phone_alt = (
            '8' + phone[2:]
            if phone.startswith('+7')
            else '+7' + phone[1:]
        )
        qs2 = User.objects.filter(phone=phone_alt)
        if self.current_user:
            qs2 = qs2.exclude(pk=self.current_user.pk)
        if qs.exists() or qs2.exists():
            raise forms.ValidationError('Этот номер телефона уже используется')
        return phone


class CustomPasswordChangeForm(PasswordChangeForm):
    pass
