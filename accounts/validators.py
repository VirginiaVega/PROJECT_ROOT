from django.core.exceptions import ValidationError
from django.utils.translation import gettext as _


class CustomMinimumLengthValidator:
    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(
                _("La contraseña debe tener al menos %(min_length)d caracteres."),
                code='password_too_short',
                params={'min_length': self.min_length},
            )

    def get_help_text(self):
        return _("La contraseña debe tener al menos %(min_length)d caracteres.") % {'min_length': self.min_length}


class CustomCommonPasswordValidator:
    def validate(self, password, user=None):
        from django.contrib.auth.password_validation import CommonPasswordValidator
        common_validator = CommonPasswordValidator()
        try:
            common_validator.validate(password)
        except ValidationError:
            raise ValidationError(_("La contraseña es demasiado común."), code='password_too_common')

    def get_help_text(self):
        return _("La contraseña no debe ser demasiado común.")


class CustomNumericPasswordValidator:
    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(
                _("La contraseña no puede contener solo números."),
                code='password_entirely_numeric',
            )

    def get_help_text(self):
        return _("La contraseña no puede contener solo números.")
