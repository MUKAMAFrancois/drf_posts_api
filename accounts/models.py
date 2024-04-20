from django.db import models
import re
from django.contrib.auth import get_user_model
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
# Create your models here.



class CustomUserManager(BaseUserManager):

    def create_user(self,email,username,password=None,bio='',photo='',**extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        if get_user_model().objects.filter(email=email).exists():
            raise ValueError('The Email is already taken')
        
        if not password:
            raise ValueError('The Password field must be set')
        password_pattern=r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@#$%^&*()-_+=])[A-Za-z\d!@#$%^&*()-_+=]{8,}$'
        if not re.match(password_pattern,password):
            raise ValueError('The Password must contain atleast one uppercase letter, one lowercase letter, one digit, one special character and must be atleast 8 characters long')
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(email=email,username=username,bio=bio,photo=photo,**extra_fields)
        user.set_password(password)
        user.save(using=self._db) # using=self._db is used to save the user in the default database for which CustomUserManager is defined
        return user
    

    def create_superuser(self,email,username,password=None,bio='',photo='',**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True')

        return self.create_user(email,username,password,bio,photo,**extra_fields)
    


class User(AbstractBaseUser,PermissionsMixin):
    """
    Custom user that uses email as the unique identifier
    with additional fields
    """

    email = models.EmailField('email adress',unique=True)
    first_name = models.CharField('first name',max_length=30,blank=True)
    last_name = models.CharField('last name',max_length=30,blank=True)
    username = models.CharField('username',max_length=30,unique=True)
    bio = models.TextField('bio',blank=True)
    photo = models.ImageField('photo',upload_to='profile_photos/',blank=True)
    is_active = models.BooleanField('active',default=True)
    is_staff = models.BooleanField('staff status',default=False)
    date_joined = models.DateTimeField('date joined',auto_now_add=True)

    objects = CustomUserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


    def __str__(self):
        return self.email