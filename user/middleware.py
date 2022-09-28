import jwt
from django.http import HttpResponsePermanentRedirect
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.AUTH_URL = '/user/auth'

    def __call__(self, request):
        try:
            token = request.COOKIES["Authorization"]  
            try:
                payload = jwt.decode(token, 'secret', algorithms=["HS256"])
                if request.path == self.AUTH_URL:
                   return  HttpResponsePermanentRedirect('/home')
            except:
                if request.path == self.AUTH_URL:
                   return self.get_response(request) 
        except:
            return HttpResponsePermanentRedirect('/user/auth')
        return self.get_response(request)
        
