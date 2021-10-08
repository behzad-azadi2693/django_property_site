from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager,PermissionsMixin
from django.core.validators import RegexValidator
import os

class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password):
        if not username:
            raise ValueError('لطفا یوزرنیم را وارد کنید')

        if not email:
            raise ValueError('لطفا ایمیل را وارد کنید')

        user = self.model(username=username, email=email)
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, password):
        user = self.create_user(username, email, password)
        user.is_admin = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(max_length=250, unique=True, verbose_name='نام کاربری')
    email = models.EmailField(unique=True, verbose_name='ایمیل')
    

    is_active = models.BooleanField(default=True, verbose_name='آیا یوزر فعال باشد?')
    is_admin = models.BooleanField(default=False, verbose_name='آیا یوزر ادمین است?')
    objects = MyUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email',]

    class Meta:
        verbose_name = 'مدل کاربر'
        verbose_name_plural = 'مدل کاربران'

    def __str__(self):
        return f'{self.username}-{self.email}'
    
    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True
        
    @property
    def is_staff(self):
        return self.is_admin


def path_save_image(instance, filename):
    ext = filename.split('.')[-1]
    name = instance.name
    name_agent = name.replace(' ','_')
    filename = f'{name_agent}.{ext}'

    return f'agents/{filename}'

class Agent(models.Model):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="فرمت موبایل مانند: '+999999999'. ")
    name = models.CharField(max_length=200)
    number = models.CharField(validators=[phone_regex], max_length=17, unique=True,verbose_name='تلفن')
    email = models.EmailField()
    description = models.TextField()
    image = models.ImageField(upload_to=path_save_image)

    class Meta:
        verbose_name = 'مشاوران'
        verbose_name_plural = 'مشاوران'

    def __str__(self) -> str:
        return self.name

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Agent, self).delete()
    
    def save(self, *args, **kwargs):
        try:
            this = Agent.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: 
            pass
        super(Agent, self).save(*args, **kwargs)