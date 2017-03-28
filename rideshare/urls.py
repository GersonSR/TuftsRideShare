"""rideshare URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import TemplateView
from django.contrib.auth import views as auth_views
from rides import views as core_views

urlpatterns = [
    url(r'^', include('rides.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^myrides/$', core_views.MyRides.as_view(), name='myrides'),
    url(r'^joinedrides/$', core_views.JoinedRides.as_view(), name='joinedrides'),
    url(r'^joinedrides/(?P<pk>[0-9]+)/leave/$', core_views.leaveride, name='leaveride'),
    url(r'^ridelist/$', core_views.AvaliableRides.as_view(), name='ridelist'),
    url(r'^ridelist/(?P<pk>[0-9]+)/$', core_views.ridedetail, name='ridedetails'),
    url(r'^profile/$', core_views.profile, name='profile'),
    url(r'^user/(?P<username>[a-zA-Z0-9]+)/$', core_views.userdetail, name='userdetails'),
    url(r'^ridelist/(?P<pk>[0-9]+)/addrider/$', core_views.addrider, name='addrider'),
    url(r'^ridelist/(?P<pk>[0-9]+)/delete/$', core_views.deleteride, name='deleteride'),
    url(r'^$', TemplateView.as_view(template_name='base.html'), name='home'),
    url(r'^create/$', core_views.create, name='create'),
    url(r'^login/$', auth_views.login, {'template_name': 'login.html'}, name='login'),
    url(r'^logout/$', auth_views.logout, {'next_page': 'home'}, name='logout'),
    url(r'^signup/$', core_views.signup, name='signup'),
    url(r'^messages/', include('postman.urls', namespace='postman', app_name='postman')),
]