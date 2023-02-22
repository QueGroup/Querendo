LANGUAGE_SESSION_KEY = '_language'
from django.utils.deprecation import MiddlewareMixin
from django.utils import translation


class UserLanguageMiddleware(MiddlewareMixin):

    def process_response(self, request, response):
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            return response

        user_language = getattr(user, 'language', None)
        if not user_language:
            return response

        current_language = translation.get_language()
        if user_language == current_language:
            return response

        translation.activate(user_language)
        request.session[LANGUAGE_SESSION_KEY] = user_language

        return response
