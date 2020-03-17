from django.shortcuts import render
from django.http import HttpResponse
import requests, json, base64

# Create your views here.
def login(request):
    if(request.method)=='POST':
        username = request.POST.get('id')
        password = request.POST.get('pwd')
        if userauth(username, password) is True:
            return HttpResponse("Success")
        else:
            return HttpResponse("Failure")
        #render(request, '../templates/login/login.html')
    return render(request, '../templates/login.html')

def userauth(id, pwd):
    password_bytes = pwd.encode('ascii')
    b64_password_bytes = base64.b64encode(password_bytes)
    b64_password = b64_password_bytes.decode('ascii')
    url = "https://login.skku.edu/loginAction"
    headers = {'Content-Type': 'application/json'}
    login_data = {'lang': 'ko', 'userid': id, 'userpwd': b64_password}
    r = requests.post(url, headers=headers, data = json.dumps(login_data))
    result = r.json()['returnCode']
    if result == 'success':
        return True
    else:
        return False
