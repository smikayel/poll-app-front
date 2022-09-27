import json
from multiprocessing import context
from django.shortcuts import render
import requests
from django.shortcuts import redirect
import jwt


BASE_URL = "http://localhost:8000/api/v1/"

#login 
def index(request):
    req = render(request, 'auth.html')
    if request.method == 'POST':
        username, password = request.POST.get('username'), request.POST.get('password')
        data ={
            "username": username,
            "password": password
        }
        responseBackend = requests.post(BASE_URL + "user/auth", headers=request.headers, data=data)
        if responseBackend.status_code != 200:
            return render(request, 'auth.html', context={"error": "Wrong email or password..."})
        else:
            request.COOKIES["Authorization"] = responseBackend.headers["Authorization"]
            req.set_cookie(key='Authorization', value=responseBackend.headers["Authorization"])
    return req


# registration
def register(request):
    headers = {"Content-Type": "application/json; charset=utf-8"}
    if request.method == "POST":
        username, password, email = request.POST.get('username'), request.POST.get('password'), request.POST.get('email')
        data = {
            "username": username,
            "password": password,
            "email": email
        }
        created_res = requests.post(BASE_URL + "user", headers=headers, data=(json.dumps(data)))
        if created_res.status_code == 200:
            return render(request, "register.html", context={"done": True})
        else:
            return render(request, "register.html", context={"error": "Try to use other email or username..."})
    return render(request, "register.html")

#delete poll request
def dell_request(request, header, poll_uuid):
    print(poll_uuid)
    delResponse = requests.delete(BASE_URL + 'poll', headers=header, data=json.dumps({"poll-uuid": poll_uuid}))



# render voted apps tru or falls
def render_voted(request, headers, payload, polls):
    voteds = requests.get(BASE_URL + "poll/voted", headers=headers)
    jsonVoted = voteds.json()["data"]
    uuidArr = []
    for voted in jsonVoted:
        uuidArr.append(voted["poll_id"])
    for poll in polls:
        if poll["uuid"] in uuidArr:
            poll["voted"] = True
    return polls

#get all pols 
def get_polls(request, headers, payload):
    resPost = requests.get( BASE_URL + "poll",  headers=headers)
    if resPost.status_code == 200:
        data = render_voted(request, headers, payload, resPost.json()["data"])
        return render(request, "home.html", context={"polls":data, "isAdmin": payload["isAdmin"]})
    else: return render(request, "home.html")

#home page
def home(request):
    headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": request.COOKIES.get('Authorization') 
    }
    token =  request.COOKIES.get('Authorization') 
    try:
        payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    except:
        return redirect('user/post')
    if request.method == "GET":
       return get_polls(request, headers, payload)
    elif request.method == "POST":
        uuid ,firstOption, secondOption = request.POST.get("uuid"), request.POST.getlist('firstOption'), request.POST.getlist('secondOption')
        if not firstOption and not secondOption:
            dell_request(request, headers, uuid)
            return get_polls(request, headers, payload)
        print(uuid ,firstOption, secondOption)
        data = {
            "option-id": (firstOption and 1) or (secondOption and 2)
        }
        responseBackend = requests.put(BASE_URL + f"poll/{uuid}", headers=headers, data=json.dumps(data))
        return get_polls(request, headers, payload)


    return render(request, "home.html")    



def adminPanel(request):
    try:
       headers = {
        "Content-Type": "application/json; charset=utf-8",
        "Authorization": request.COOKIES.get('Authorization') 
        }
    except:
        return redirect('user/auth')
    token = request.COOKIES["Authorization"]
    payload = jwt.decode(token, 'secret', algorithms=["HS256"])
    if payload["isAdmin"] == False:
        return redirect('pols')
    
    if request.method == "GET":
        all_data = requests.get(f"http://localhost:8000/api/v1/poll", headers=headers)
        pages = len(all_data.json()["data"]) / 10
        if pages <= 10:
            pages = 1
        return render(request, "admin.html")

    if request.method == "POST":
        title, firstOption, secondOption = request.POST.get('title'), request.POST.get('firstOption'), request.POST.get('secondOption')
        data = {
            "title": title,
            "firstOption": firstOption,
            "secondOption": secondOption
        }
        creaetd = requests.post(f"http://localhost:8000/api/v1/poll", headers=headers, data=json.dumps(data))
        if creaetd.status_code == 200:
            return render(request, "admin.html", context={"done": True})
        else:
            return render(request, "admin.html")
    