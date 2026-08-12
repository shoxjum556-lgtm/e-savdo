from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User


class UzbekLoginForm(AuthenticationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        widget=forms.TextInput(attrs={"placeholder": "Foydalanuvchi nomingiz"}),
    )
    password = forms.CharField(
        label="Parol",
        widget=forms.PasswordInput(attrs={"placeholder": "Parolingiz"}),
    )

    error_messages = {
        "invalid_login": "Foydalanuvchi nomi yoki parol noto'g'ri.",
        "inactive": "Bu akkaunt faol emas.",
    }


class UzbekRegisterForm(UserCreationForm):
    username = forms.CharField(
        label="Foydalanuvchi nomi",
        help_text="",
        widget=forms.TextInput(attrs={"placeholder": "Foydalanuvchi nomini kiriting"}),
    )
    password1 = forms.CharField(
        label="Parol",
        help_text="",
        widget=forms.PasswordInput(attrs={"placeholder": "Parol yarating"}),
    )
    password2 = forms.CharField(
        label="Parolni tasdiqlash",
        help_text="",
        widget=forms.PasswordInput(attrs={"placeholder": "Parolni qayta kiriting"}),
    )

    class Meta:
        model = User
        fields = ("username", "password1", "password2")

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError("Bu foydalanuvchi nomi allaqachon mavjud.")
        return username

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Parollar bir-biriga mos kelmaydi.")
        return password2
