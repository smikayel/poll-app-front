from time import sleep
import jwt
from django.http import HttpResponsePermanentRedirect
class CustomMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.NON_PROTECTED = ['/user/auth', '/register']

    def __call__(self, request):
        if request.path not in self.NON_PROTECTED:
            try:
                token = request.COOKIES["Authorization"]
                payload = jwt.decode(token, 'secret', algorithms=["HS256"])
                return self.get_response(request)
            except:
                return HttpResponsePermanentRedirect('/user/auth') 
        else:
            try:
                token = request.COOKIES["Authorization"]
                payload = jwt.decode(token, 'secret', algorithms=["HS256"])
                flag = True
            except:
                flag = False
            if not flag:
                return self.get_response(request)
            else:
                return HttpResponsePermanentRedirect('/home') 

        
        
        
        
        
        
        
        # flag = False
        # try:
        #     token = request.COOKIES["Authorization"]
        #     payload = jwt.decode(token, 'secret', algorithms=["HS256"])
        # except:
        #     flag = True
        # if request.path !=  self.AUTH_URL:
        #     return self.get_response(request)
        # else:
        #     if flag:
        #         return HttpResponsePermanentRedirect('/user/auth')
        #     return HttpResponsePermanentRedirect('/home')
        # except:
        #     return HttpResponsePermanentRedirect('/user/auth')
