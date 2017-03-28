from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rides import views

urlpatterns = [
    # url(r'^rides/$', views.RideList.as_view()),
    # url(r'^rides/(?P<pk>[0-9]+)/$', views.RideDetail.as_view()),
    # url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)