from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _


class PINCodeValidator(object):
    def validate(self, password, user=None):
        if password[:4].isdigit():
            raise ValidationError(
                _("This password must be exactly 4 numbers."),
                code='Invalid password length'
            )

    def get_help_text(self):
        return _(
            "Your pincode must contain at exactly 4 numbers."
            % {'min_length': self.min_length}
        )
