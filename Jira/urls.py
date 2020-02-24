from django.conf.urls import url
from Jira import views
app_name = 'Jira'
urlpatterns = [
  url(r'^$', views.home, name='home'),
  url(r'^home/$', views.home, name='home'),
  url(r'^gettoken/$', views.gettoken, name='gettoken'),
  url(r'^issues$',views.issueviewer, name='issueviewer'),
  url(r'^cissues$',views.cissues,name='cissues'),
  url(r'^issueset$',views.issueset,name="issueset"),
  url(r'^getissuetypes/$',views.getissuetypes,name="getissuetypes"),
]