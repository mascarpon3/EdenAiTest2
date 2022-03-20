from rest_framework.authtoken.models import Token


def get_user_from_post_request(post_request):
    key = post_request.META["HTTP_AUTHORIZATION"].replace("Token ", "")
    user = Token.objects.get(key=key).user
    return user
