from rest_framework_simplejwt.tokens import AccessToken, TokenError

def verify_token(token):
    try:
        decoded_token = AccessToken(token)
        return decoded_token
    except TokenError as e:
        return str(e)