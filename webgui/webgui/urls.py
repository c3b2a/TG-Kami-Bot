from django.contrib import admin
from django.urls import path,re_path
from django.conf.urls import url
from django.conf.urls.static import static
from django.conf import settings

from . import index_page,err_page,login,logout,panel,redirect,myid

urlpatterns = [
	re_path(r'^$',index_page.index),
    re_path(r'^login/?$',login.Login),
    re_path(r'^404/?$',err_page.page_404),
    re_path(r'^500/?$',err_page.page_500),
    re_path(r'^panel/\w+?/?$|^panel/?$',panel.panel),
    re_path(r'^logout/?$',logout.Logout),
    re_path(r'^myid/?$',myid.showid),
    re_path(r'^redirect$',redirect.process),
]

hander404 = "users.err_page.page_404"
hander500 = "users.err_page.page_500"
