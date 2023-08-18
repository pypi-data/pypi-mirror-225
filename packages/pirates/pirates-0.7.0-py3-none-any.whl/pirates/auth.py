from mozilla_django_oidc.auth import OIDCAuthenticationBackend

from .signals import post_login


class PiratesOIDCAuthenticationBackend(OIDCAuthenticationBackend):
    """
    Pirates OIDC Authentication Backend.

    Instead of `email` uses claim `sub` (as `sso_id`) to identify users. Which
    allows for email change.
    """

    def get_sso_id(self, claims):
        return claims.get("sub")

    def filter_users_by_claims(self, claims):
        sso_id = self.get_sso_id(claims)
        if not sso_id:
            return self.UserModel.objects.none()
        return self.UserModel.objects.filter(sso_id=sso_id)

    def create_user(self, claims):
        sso_id = self.get_sso_id(claims)
        first_name = claims.get("given_name", "")
        last_name = claims.get("family_name", "")
        email = claims.get("email", "")
        user = self.UserModel.objects.create(
            sso_id=sso_id, first_name=first_name, last_name=last_name, email=email
        )
        self.send_post_login_signal(user, True, claims)
        return user

    def update_user(self, user, claims):
        user.first_name = claims.get("given_name", "")
        user.last_name = claims.get("family_name", "")
        user.email = claims.get("email", "")
        user.save()
        self.send_post_login_signal(user, False, claims)
        return user

    def send_post_login_signal(self, user, created, claims):
        post_login.send(
            sender=self.__class__,
            user=user,
            created=created,
            claims=claims,
            request=self.request,
        )
