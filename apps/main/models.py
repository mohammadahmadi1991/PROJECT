from django.db import models
from django.utils import timezone
from apps.account.models import CustomUser
# Create your models here.

class Blog(models.Model):
    blog_title= models.CharField(max_length=1000,verbose_name="Title")
    blog_text= models.TextField(verbose_name="Text")
    main_img=models.ImageField(upload_to='image/blogimg/',verbose_name="Image",default=None)
    register_date=models.DateTimeField(default=timezone.now)
    user_registered=models.ForeignKey(CustomUser, on_delete=models.CASCADE)
