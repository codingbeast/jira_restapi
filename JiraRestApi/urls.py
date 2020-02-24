from django.contrib import admin
from django.urls import path
from django.conf.urls import url,include
from Jira import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^$',views.loginpage,name='loginpage'),
    url(r'^jira/',include("Jira.urls",namespace="Jira")),
]
