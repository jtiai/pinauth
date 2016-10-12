from django.contrib.auth import backends, get_user_model
import pyotp


class PINCodeBackend(backends.ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        if username is None:
            username = kwargs.get(UserModel.USERNAME_FIELD)
        try:
            user = UserModel._default_manager.get_by_natural_key(username)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a non-existing user (#20760).
            UserModel().set_password(password[:4])
        else:
            if user.check_password(password[:4]) and self.user_can_authenticate(user):
                # Check the TOTP key part
                totp = pyotp.TOTP(user.psk.secret_key)
                print(user.psk.secret_key, password[4:], totp.verify(password[4:]))
                if totp.verify(password[4:]):
                    return user
