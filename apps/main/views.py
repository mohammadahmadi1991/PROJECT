from django.shortcuts import render,redirect
from django.conf import settings
from .models import Blog
from apps.account.models import CustomUser
from .forms import BlogForm
from django.core.files.storage import FileSystemStorage
import os 
import datetime
from django.contrib.auth.decorators import login_required
from django.shortcuts import render,get_object_or_404
# -------------------------------------------------------------
def showblog(request):
    blogs=Blog.objects.order_by('id').reverse()
    if request.user.is_authenticated:
        userInfo=CustomUser.objects.get(email=request.user.email)
    else:
        userInfo='Null'
    context={
        "blogs":blogs,
        'media_url':settings.MEDIA_URL,
        'info':userInfo
    }
    return render(request,"main_app/index.html",context)

#-----------------------------------------------------------------------
@login_required
def create_blog(request):
    userInfo=CustomUser.objects.get(email=request.user.email)
    if request.method=="POST":
        form = BlogForm(request.POST,request.FILES)
        if form.is_valid():
            imageUpload = request.FILES['main_img']
            imgName , ext = os.path.splitext(imageUpload.name)
            currenttime = datetime.datetime.utcnow().strftime("%Y%m%d%H%M%S%f")
            imagePath = 'image/blogimg/'+imgName+currenttime+ext
            data=form.cleaned_data
            blog=Blog()
            blog.blog_title=data['blog_title']
            blog.blog_text=data['blog_text']
            blog.main_img=imagePath
            blog.user_registered=request.user
            blog.save()
            fss=FileSystemStorage()
            fss.save(imagePath,imageUpload) 
            return redirect('main:index')
    else:
        form=BlogForm()
        context={
            'form':form,
            'info':userInfo,
            'media_url':settings.MEDIA_URL
        }
        return render(request,'main_app/register_blog.html',context)

#-----------------------------------------------------------------------
@login_required
def profile(request):
    list1=[]
    userInfo=CustomUser.objects.get(email=request.user.email)
    blogs=Blog.objects.order_by('id').reverse()
    for item in blogs:
        if item.user_registered.email == userInfo.email:
            list1.append(item)
            
            
    context={'info':userInfo,'media_url':settings.MEDIA_URL,"blogs":list1}
    
    return render(request,'main_app/profile.html',context)

#-----------------------------------------------------------------------
def infouser(request,user_id):
    list1=[]
    userInfo = get_object_or_404(CustomUser,email=user_id)
    blogs=Blog.objects.order_by('id').reverse()
    for item in blogs:
        if item.user_registered.email == user_id:
            list1.append(item)
    context={'info':userInfo,'media_url':settings.MEDIA_URL,"blogs":list1}
    return render(request,"main_app/profile.html",context)
#-----------------------------------------------------------------------

def article_detail(request,article_id):
    article = get_object_or_404(Blog,blog_title=article_id)
    return render(request,"main_app/mainblog.html",{'article':article,'media_url':settings.MEDIA_URL})
