from authentications.managers import AuthenticationUserManager


class UserManager(AuthenticationUserManager):
    """Custom user manager for filtering user accounts."""

    def get_queryset(self):
        return super().get_queryset().filter(is_deleted=False)
