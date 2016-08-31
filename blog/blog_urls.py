from django.conf.urls import url,include
from .views import (
	post_list,post_detail,post_create,post_update,post_delete,UserFormView,LoginFormView,user_logout,myposts
	)

urlpatterns = [
    
    url(r'^$', post_list,name="post_list"),
    url(r'^posts/$', post_list,name="post_list"),
    url(r'^myposts/$', myposts,name="myposts"),


    url(r'^posts/(?P<id>\d+)/$', post_detail,name="post_detail"),
    url(r'^posts/create/$', post_create,name="post_create"),
    url(r'^posts/(?P<id>\d+)/edit/$', post_update,name="post_update"),
    url(r'^posts/(?P<id>\d+)/delete/$', post_delete,name="post_delete"),
    url(r'^register/$', UserFormView, name='register'),
    url(r'^login/$', LoginFormView, name='login'),
    url(r'^logout/$', user_logout, name='logout'),
]