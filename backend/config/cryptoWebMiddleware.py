from django.utils.deprecation import MiddlewareMixin


class CryptoWebMiddleware(MiddlewareMixin):

    def process_request(self, request):
        return
