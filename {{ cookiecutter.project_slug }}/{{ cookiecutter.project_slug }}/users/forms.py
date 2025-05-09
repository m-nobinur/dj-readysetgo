from allauth.account import app_settings
from allauth.account.forms import LoginForm
from allauth.account.forms import SignupForm
from allauth.socialaccount.forms import SignupForm as SocialSignupForm
from allauth.utils import set_form_field_order
from django import forms
from django.contrib.auth import forms as admin_forms
from django.utils.translation import gettext_lazy as _

from .models import User
from .utils import PasswordField
from .utils import login_field_css_classes
from .utils import login_password_css_classes
from .utils import name_field_css_classes
from .utils import remember_me_css_classes


class UserAdminChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):  # type: ignore[name-defined]
        model = User
        field_classes = {"email": forms.EmailField}


class UserAdminCreationForm(admin_forms.UserCreationForm):
    """
    Form for User Creation in the Admin Area.
    To change user signup, see UserSignupForm and UserSocialSignupForm.
    """

    class Meta(admin_forms.UserCreationForm.Meta):  # type: ignore[name-defined]
        model = User
        fields = ("email",)
        field_classes = {"email": forms.EmailField}
        error_messages = {
            "email": {"unique": _("This email has already been taken.")},
        }


class UserLoginForm(LoginForm):
    def __init__(self, *args, **kwargs) -> None:
        self.request = kwargs.pop("request", None)
        super(LoginForm, self).__init__(*args, **kwargs)

        login_widget = forms.TextInput(
            attrs={
                "type": "email",
                "placeholder": _("Email address"),
                "autocomplete": "email",
                "autofocus": "autofocus",
                "class": login_field_css_classes,
            },
        )
        login_field: forms.EmailField | forms.CharField = forms.EmailField(
            label=_("Email"),
            widget=login_widget,
        )
        remeber_widget = forms.CheckboxInput(attrs={"class": remember_me_css_classes})
        password_widget = forms.PasswordInput(
            attrs={
                "placeholder": _("Password"),
                "autocomplete": "current-password",
                "class": login_password_css_classes,
            },
        )
        remeber_field = forms.CharField(
            widget=remeber_widget,
            required=False,
        )
        password_field = forms.CharField(
            widget=password_widget,
            required=True,
        )

        self.fields["remember"] = remeber_field
        self.fields["login"] = login_field
        self.fields["password"] = password_field
        set_form_field_order(self, ["login", "password", "remember"])
        if app_settings.SESSION_REMEMBER is not None:
            del self.fields["remember"]


class UserSignupForm(SignupForm):
    first_name = forms.CharField(
        max_length=30,
        label="First Name",
        widget=forms.TextInput(
            attrs={"placeholder": _("First Name"), "class": name_field_css_classes},
        ),
    )
    last_name = forms.CharField(
        max_length=30,
        label="Last Name",
        widget=forms.TextInput(
            attrs={"placeholder": _("Last Name"), "class": name_field_css_classes},
        ),
    )

    def __init__(self, *args, **kwargs) -> None:
        super(SignupForm, self).__init__(*args, **kwargs)

        email_field = forms.EmailField(
            label=_("Email Address"),
            widget=forms.TextInput(
                attrs={
                    "type": "email",
                    "placeholder": _("E-mail address"),
                    "class": name_field_css_classes,
                },
            ),
        )

        self.fields["email"] = email_field
        self.fields["password1"] = PasswordField(
            label=_("Password"),
            autocomplete="new-password",
        )
        if app_settings.SIGNUP_PASSWORD_ENTER_TWICE:
            self.fields["password2"] = PasswordField(
                label=_("Repeat Password"),
                autocomplete="new-password",
            )

        if hasattr(self, "field_order"):
            set_form_field_order(self, self.field_order)

    def save(self, request):  # pragma: no cover Already tested via django-allauth
        user: User = super().save(request)
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        user.name = f"{user.first_name} {user.last_name}"
        user.save()
        return user


class UserSocialSignupForm(SocialSignupForm):
    """
    Renders the form when user has signed up using social accounts.
    Default fields will be added automatically.
    See UserSignupForm otherwise.
    """
