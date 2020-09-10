from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from accounts.models import Users
import logging

class CustomBackend(BaseBackend):
    """
    Authenticate against the Custome User model
    Use the login name and a hash of the password. For example:
    """

    def authenticate(self, request, email=None, password=None):
            try:
                user = Users.objects.get(email=email)
                if user.check_password(password):
                    return user
                else:
                    return None
            except Users.DoesNotExist:
                # Create a new user. There's no need to set a password
                # because only the password from settings.py is checked.
                # logging.getLogger("error_logger").error("user with login %s does not exists " % login)
                return None
            except Exception as e:
                logging.getLogger("error_logger").error(repr(e))
                return None

    def get_user(self, user_id):
        try:
            user = Users.objects.get(id=user_id)
            if user.is_active:
                return user
            return None
        except Users.DoesNotExist:
            logging.getLogger("error_logger").error("user with %(user_id)d not found")
            return None