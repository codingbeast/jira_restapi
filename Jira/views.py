from django.shortcuts import render
from django.shortcuts import render
from django.shortcuts import HttpResponse,HttpResponseRedirect,redirect
from django.urls import reverse
from uuid import uuid4
from Jira import views
import requests
import json
import time
from Jira import jiraservices
from Jira import outhhelper
from django.views.decorators.csrf import csrf_exempt
def loginpage(request):
    state = str(uuid4())
    myappurl="https://auth.atlassian.com/authorize?audience=api.atlassian.com&client_id=etjwdVpGiOCKgTHBFYIeYv5fh887k4e0&scope=read%3Ajira-user%20read%3Ajira-work%20manage%3Ajira-project%20write%3Ajira-work%20manage%3Ajira-configuration%20manage%3Ajira-data-provider&redirect_uri=http%3A%2F%2Flocalhost%3A8000%2Fjira%2Fgettoken%2F&state=${}&response_type=code&prompt=consent".format(state)
    context={
        "signin_url" : myappurl,
    }
    return render(request,"home.html",context)
def gettoken(request):
    code=request.GET['code']
    outhhelper.save_token_from_code(request,code)
    rdi=reverse("Jira:home")
    return HttpResponseRedirect(rdi)
def save_created_state(state):
	pass
def is_valid_state(state):
	return True
def home(request):
    rdi_status,access_token=outhhelper.get_token(request)
    if rdi_status==True:
        return HttpResponseRedirect(access_token)
    else:
        pass
    userinfo=jiraservices.resources(access_token)
    myid=userinfo['id']
    request.session['myid'] = myid
    myprojects=jiraservices.projects(access_token,myid)
    issue_rdi=reverse("Jira:issueviewer")
    context={
        "ProjectsDetails" : myprojects,
        "url" : issue_rdi,
    }
    return render(request,"userinfo.html",context)
    #return HttpResponse(access_token)
def issueviewer(request):
    rdi_status,access_token=outhhelper.get_token(request)
    if rdi_status==True:
        return HttpResponseRedirect(access_token)
    else:
        pass
    project_code=request.GET['gid']
    client_id=request.session['myid']

    issues=jiraservices.getIssues(access_token,project_code,client_id)
    context={
        "issues" : issues
    }
    return render(request,"issues.html",context)
def cissues(request):
    try:
        rdi_status,access_token=outhhelper.get_token(request)
        myid=request.session['myid']
    except:
        return HttpResponseRedirect("/")
    myprojects=jiraservices.projects(access_token,myid)
    context={
        "ProjectsDetails" : myprojects,
    }
    return render(request,"ctissues.html",context)
@csrf_exempt
def issueset(request):
  if request.method=="POST":
    project_code=request.POST['selectproject']
    summary=request.POST['summary']
    description=request.POST['description']
    issueType=request.POST['issuetype']
    client_id=request.session['myid']
    #return HttpResponse(issueType)

    access_token=request.session['access_token']
    issueadd=jiraservices.isssueadd(access_token,client_id,project_code,summary,description,issueType)
    try:
        issueadd=issueadd.json()
        issueid=issueadd['id']
        issue_rdi=reverse("Jira:issueviewer")
        rdi=issue_rdi+"?gid="+project_code
        return HttpResponseRedirect(rdi)
    except Exception as e:
        error=reverse("Jira:getissuetypes")
        return HttpResponseRedirect(error)
def getissuetypes(request):
    try:
        client_id=request.session['myid']
    except:
        return HttpResponseRedirect("/")
    rdi_status,access_token=outhhelper.get_token(request)
    if rdi_status==True:
        return HttpResponseRedirect(access_token)
    else:
        pass
    
    rdi_status,access_token=outhhelper.get_token(request)
    if rdi_status==True:
        return HttpResponseRedirect(access_token)
    myid=request.session['myid']
    myprojects=jiraservices.projects(access_token,myid)
    projectCode=[i['key'] for i in myprojects]
    issuetypesdata={}
    for project_id in projectCode:
        data=jiraservices.getIssueType(access_token,client_id,project_id)
        data_temp=list(data)
        issuetypesdata[project_id]=data_temp
    context={
        "id" : projectCode,
        "issuetype" : issuetypesdata,
    }
    return render(request,"error.html", context)

