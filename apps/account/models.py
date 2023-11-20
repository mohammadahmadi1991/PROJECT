from django.db import models
from django.contrib.auth.models import BaseUserManager , AbstractBaseUser


class CustomUserManager(BaseUserManager):
    def create_user(self, email,image_url,password=None):
        if not email:
            raise ValueError('Users must have an email address')
        
        user= self.model(
            email= self.normalize_email(email),
            image_url=image_url
        )
        
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self,email,image_url,password=None):
        user= self.create_user(
             email,
             password=password,
             image_url=image_url
        )
        user.save(using=self._db)
        return user
     
     
# -----------------------------------------------------------------
class CustomUser(AbstractBaseUser):
    email = models.EmailField(max_length=200,primary_key=True,unique=True)
    image_url= models.TextField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    objects=CustomUserManager()
    def __str__(self):
        return f'{self.email},{self.image_url}'
    
    def has_perm(self,perm, obj=None):
        return True
    
    def has_module_perms(self, app_label):
        return True
    
    # @property
    # def is_staff(self):
    #     return self.is_admin
    
    