import requests
import json
import time
from django.urls import reverse
def get_token(request):
    rdi_status=True
    rdi=reverse("loginpage")
    try:
        current_token = request.session['access_token']
        expiration = request.session['token_expires']
        now = int(time.time())
        if (current_token and now < expiration):
            # Token still valid
            rdi_status=False
            return rdi_status,current_token
        else:
            rdi_status=False
            myoldtoken=current_token
            token=refresh_token(request,myoldtoken)
            return rdi_status,token
    except:
        return rdi_status,rdi
def save_token_from_code(request,code):
    token=get_token_from_code(code)
    access_token = token['access_token']
    expires_in = token['expires_in']
    expiration = int(time.time()) + expires_in - 300
    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['token_expires'] = expiration
    return access_token
def get_token_from_code(code):
    url="https://auth.atlassian.com/oauth/token"
    headers = {
        "Content-Type" : "application/json"
    }
    parameters={
        "grant_type": "authorization_code",
        "client_id": "etjwdVpGiOCKgTHBFYIeYv5fh887k4e0",
        "client_secret": "RI17O1fq9PZC_VZs7xOHtWFOsmNDM73hvhDiDswb_GdcC72VjLESY1Y8UyValTQE",
        "code": code,
        "redirect_uri": "http://localhost:8000/jiracreater/gettoken/"
    }
    response = requests.post(url, headers = headers, data =json.dumps(parameters), params =  parameters).json()
    return response
def refresh_token(request,myoldtoken):
    url="https://auth.atlassian.com/oauth/token"
    headers = {
        "Content-Type" : "application/json"
    }
    parameters={
        "grant_type": "refresh_token", 
        "client_id": "etjwdVpGiOCKgTHBFYIeYv5fh887k4e0",
        "client_secret": "RI17O1fq9PZC_VZs7xOHtWFOsmNDM73hvhDiDswb_GdcC72VjLESY1Y8UyValTQE",
        "refresh_token": myoldtoken
    }
    token = requests.post(url, headers = headers, data =json.dumps(parameters), params =  parameters).json()
    access_token = token['access_token']
    expires_in = token['expires_in']
    expiration = int(time.time()) + expires_in - 300
    # Save the token in the session
    request.session['access_token'] = access_token
    request.session['token_expires'] = expiration
    return access_token
