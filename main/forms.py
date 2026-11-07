from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User
from .models import Profile


class AccountForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")
        labels = {
            "username": "Username",
            "email": "Email",
        }
        widgets = {
            "username": forms.TextInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-[#0108A1]",
            }),
            "email": forms.EmailInput(attrs={
                "class": "w-full rounded-xl border border-gray-300 px-4 py-3 outline-none focus:border-[#0108A1]",
            }),
        }


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("foto",)
        labels = {"foto": "Foto Profil (opsional)"}
        widgets = {
            "foto": forms.ClearableFileInput(attrs={
                "class": "block w-full rounded-xl border border-gray-300 bg-gray-50 px-4 py-3 text-sm text-gray-700",
                "accept": "image/*",
            }),
        }


class AccountPasswordForm(PasswordChangeForm):
    class Meta:
        labels = {
            "old_password": "Password Lama",
            "new_password1": "Password Baru",
            "new_password2": "Konfirmasi Password Baru",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        input_class = (
            "w-full rounded-xl border border-gray-300 px-4 py-3 outline-none "
            "focus:border-[#0108A1]"
        )
        for field in self.fields.values():
            field.widget.attrs["class"] = input_class
        self.fields["old_password"].label = "Password Lama"
        self.fields["new_password1"].label = "Password Baru"
        self.fields["new_password2"].label = "Konfirmasi Password Baru"
