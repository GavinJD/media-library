from django import forms
from django.contrib.auth.forms import UserCreationForm
import users.models


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = users.models.User
        fields = UserCreationForm.Meta.fields
