from typing import Any
from django import http
from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterUserForm,LoginUserForm
from .models import CustomUser
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.conf import settings

class RegisterUserView(View):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated :
            return redirect('main:index')
        return super().dispatch(request,*args,**kwargs)
    
    def get(self,request,*args,**kwargs):
        form=RegisterUserForm()
        return render(request,"accounts_app/register.html",{"form":form,'media_url':settings.MEDIA_URL})
    
    
    def post(self,request, *args , **kwargs):
        form=RegisterUserForm(request.POST , request.FILES)
        if form.is_valid():
            user=form.cleaned_data
            CustomUser.objects.create_user(
                email=user['email'],
                password=user['password'],
                image_url=user['image_url']
            )
            
            return redirect('main:login')
        else:
            messages.error(request,'The information is not valid!','error')
            return render(request,"accounts_app/register.html",{"form":form,'media_url':settings.MEDIA_URL})
# -----------------------------------------------------------------
class LoginUserView(View):
    def dispatch(self,request,*args,**kwargs):
        if request.user.is_authenticated :
            return redirect('main:index')
        return super().dispatch(request,*args,**kwargs)
    
    def get(self ,request, *args,**kwargs):
        form=LoginUserForm()
        return render(request,"accounts_app/login.html",{"form":form,'media_url':settings.MEDIA_URL})
    
    def post(self, request,*args ,**kwargs):
        form=LoginUserForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            user=authenticate(username=cd.get('email'),password=cd.get('password'))
            if user is not None:                
                
                login(request,user)
                next_url=request.GET.get('next')
                if next_url is not None:
                    return redirect(next_url)
             
                else:
                    return redirect('main:index')
                   
            else:
                messages.warning(request,'The username or password is incorrect!')
                return render(request,"accounts_app/login.html",{"form":form,'media_url':settings.MEDIA_URL})
                
        else:
            messages.warning(request,'The information is invalid!')
            return render(request,"accounts_app/login.html",{"form":form,'media_url':settings.MEDIA_URL})
            
            
# -----------------------------------------------------------
class LogoutUserView(View):
    def dispatch(self,request,*args,**kwargs):
        if not request.user.is_authenticated :
            return redirect('main:index')
        return super().dispatch(request,*args,**kwargs)
    
    
    def get(self,request,*args,**kwargs):
        logout(request)
        return redirect('main:index')
