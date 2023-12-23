# Import all requirements
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.cache import cache
from django.utils import timezone
from django.conf import settings
from django.db import models
from django import forms


# Custom User Manager class
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Enter Email:')
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


USER_CATEGORY = ((0, "پرسنل انبار اخلاقی"), (1, "پرسنل انبار پلاک ۳"), (2, "پرسنل انبار مغازه غدیر"), (3, "انباردار / حسابدار"), (4, "توسعه / مدیریت"))

class user_accounts(AbstractBaseUser, PermissionsMixin):
    email = models.CharField(max_length=120,unique=True, verbose_name='پست الکترونیک')
    first_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام')
    last_name = models.CharField(max_length=100, blank=True, null=True, verbose_name='نام خانوادگی')
    phoneNumber = models.CharField(max_length=20, unique=True, verbose_name='شماره تماس')
    codeMelli = models.CharField(max_length=20, unique=True, verbose_name='کد ملی')
    is_active = models.BooleanField(default=True, verbose_name='وضعیت کاربر')
    is_staff = models.BooleanField(default=False, verbose_name='وضعیت راهبری')
    is_inventor = models.BooleanField(default=False, verbose_name='انبار دار')
    is_calculator = models.BooleanField(default=False, verbose_name='حسابدار')
    status = models.BooleanField(null=True, verbose_name='وضعیت')
    category = models.IntegerField(choices=USER_CATEGORY, default=0, verbose_name='دسته پرسنلی')
    last_activity = models.DateTimeField(null=True, blank=True)
    date_joined = forms.DateTimeField(
        label='Date Joined',
        widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
    )
    last_login = models.DateTimeField(auto_now_add=True, verbose_name='آخرین فعالیت')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
            return self.email

    def set_online(self):
        self.status = True
        self.last_activity = timezone.now()
        self.save()

    def set_offline(self):
        self.status = False
        self.save()
            
    class Meta:
        verbose_name = 'کاربر'
        verbose_name_plural = 'کاربران سایت'