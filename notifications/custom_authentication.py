from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed
from django.utils.translation import gettext_lazy as _

class CustomTokenAuthentication(TokenAuthentication):
    keyword = 'Token'
    print('this is in custom')
    def authenticate_credentials(self, key):
        model = self.get_model()
        try:
            token = model.objects.select_related('user').get(key=key)
            print('this is in token')
        except model.DoesNotExist:

            raise AuthenticationFailed(_('Invalid token.'))

        if not token.user.is_active:
            raise AuthenticationFailed(_('User inactive or deleted.'))
        print(token.user.id , '----',token ,'from custom')

        # return the user id instead of the email
        return token.user.id, token