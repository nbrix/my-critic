from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from allauth.account.forms import LoginForm 
from django.utils.translation import gettext, gettext_lazy as _, pgettext
from django import forms   

class CustomLoginForm(LoginForm):

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop("request", None)
        super().__init__(*args, **kwargs)
        login_widget = forms.TextInput(
                attrs={"placeholder": _("Username or e-mail"), "autocomplete": "email"}
            )
        login_field = forms.CharField(
            label=pgettext("field label", "Username or E-mail"), widget=login_widget
        )
        self.fields["login"] = login_field


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', )

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = get_user_model()
        fields = ('email', 'username', )