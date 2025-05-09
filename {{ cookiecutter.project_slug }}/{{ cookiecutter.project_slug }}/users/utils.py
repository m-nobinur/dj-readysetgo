from allauth.account import app_settings
from django import forms

# Basic input styling using daisyUI
name_field_css_classes: str = (
    "input input-bordered w-full"
)

password_field_css_classes: str = (
    "input input-bordered w-full"
)

login_field_css_classes: str = (
    "input input-bordered w-full"
)

login_password_css_classes: str = (
    "input input-bordered w-full"
)

remember_me_css_classes: str = (
    "checkbox"
)


class PasswordField(forms.CharField):
    def __init__(self, *args, **kwargs) -> None:
        render_value = kwargs.pop(
            "render_value",
            app_settings.PASSWORD_INPUT_RENDER_VALUE,
        )
        kwargs["widget"] = forms.PasswordInput(
            render_value=render_value,
            attrs={
                "placeholder": kwargs.get("label"),
                "class": password_field_css_classes,
            },
        )
        autocomplete = kwargs.pop("autocomplete", None)
        if autocomplete is not None:
            kwargs["widget"].attrs["autocomplete"] = autocomplete
        super().__init__(*args, **kwargs)
