from django.urls import path
from . import views

app_name='main'
urlpatterns=[
    path('',views.showblog,name="index"),
    path('registerblog/',views.create_blog,name="registerblog"),
    path('profile/',views.profile,name="profile"),
    path('infouser/<str:user_id>/',views.infouser,name="infouser"),
    path('article/<str:article_id>/',views.article_detail,name="article_detail"),
    path('profile/<str:article_id>/',views.article_detail,name="article_detail"),


]