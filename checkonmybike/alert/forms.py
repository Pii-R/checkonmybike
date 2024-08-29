from django import forms
from django.contrib.auth.models import User
from .models import Profile


class UserProfileForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(required=False)
    password = forms.CharField(widget=forms.PasswordInput, required=False)

    class Meta:
        model = Profile
        fields = []  # Add any Profile-specific fields you want to include

    def save(self, commit=True):
        # Create the User first
        user = User.objects.create_user(
            username=self.cleaned_data["username"],
            email=self.cleaned_data["email"],
            password=self.cleaned_data["password"],
        )

        # Create the Profile and associate it with the new user
        profile = super().save(commit=False)
        profile.user = user

        if commit:
            profile.save()

        return profile
