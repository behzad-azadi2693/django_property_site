from django.db import models
from uuid import uuid4

from django.db.models.fields import BLANK_CHOICE_DASH
from accounts.models import Agent
from location_field.models.spatial import LocationField
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.fields import PointField, GeometryField

class Category(models.Model):
    name = models.CharField(max_length=250, verbose_name='دسته بندی')

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'

    def __str__(self):
        return self.name

class Availability(models.Model):
    name = models.CharField(max_length=250, verbose_name='ملزومات')

    class Meta:
        verbose_name = 'ملزومات'
        verbose_name_plural = 'ملزومات'

    def __str__(self):
        return self.name


def path_save_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.code}-{instance.pk}.{ext}'
    return f'property/{instance.code}/{filename}'

class Property(models.Model):
    CHOICE = (
        ('buy','خرید'),
        ('sale','فروش'),
        ('rent','اجاره'),
        ('mort','رهن'),
    )
    CHOICE_NOW = (
        ('active', 'فعال'),
        ('sold','فروخته شد'),
        ('was_rented','اجاره داده شد'),
        ('bought','خریداری کرد'),
    )
    name = models.CharField(max_length=100, verbose_name='نام')
    code = models.UUIDField(default=uuid4, unique=True, verbose_name='کد')
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name="property_category",verbose_name='دسته بندی')
    availability = models.ManyToManyField(Availability, verbose_name='ملزومات', related_name='property_avail')
    agent = models.ForeignKey(Agent,on_delete=models.DO_NOTHING, verbose_name='مشاور')
    address = models.CharField(max_length=300, verbose_name='آدرس')
    description = models.TextField(verbose_name='توضیحات')
    price = models.PositiveBigIntegerField(verbose_name='قیمت')
    title = models.CharField(max_length=200, verbose_name='توضیحات کوتاه خانه')
    image = models.ImageField(upload_to=path_save_image , verbose_name='تصویر اصلی')
    rating = models.IntegerField(verbose_name='امتیاز')
    status = models.CharField(max_length=4, choices=CHOICE, verbose_name='وضعیت')
    is_status_now = models.CharField(max_length=10, choices=CHOICE_NOW, verbose_name='وضعیت فعلی')
    date = models.DateField(auto_now_add=True)
    location = LocationField(null=True, blank=True, based_fields=['city'], zoom=7, default=Point(35.31, 46.99))

    class Meta:
        verbose_name = 'املاک'
        verbose_name_plural = 'املاک'

    def __str__(self):
        return self.name
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Property, self).delete()
    
    def save(self, *args, **kwargs):
        try:
            this = Property.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: 
            pass
        super(Property, self).save(*args, **kwargs)


def path_save_images(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.property.code}-{instance.id}.{ext}'
    return f'property/{instance.property.code}/{filename}'

class Images(models.Model):
    property = models.ForeignKey(Property, on_delete=models.CASCADE, related_name='property_image')
    image = models.ImageField(upload_to=path_save_images)

    class Meta:
        verbose_name = 'تصاویر'
        verbose_name_plural = 'تصاویر'

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Images, self).delete()
    
    def save(self, *args, **kwargs):
        try:
            this = Images.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()
        except: 
            pass
        super(Images, self).save(*args, **kwargs)


class Email(models.Model):
    code = models.ForeignKey(Property, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.PositiveIntegerField()
    message = models.TextField()

    class Meta:
        verbose_name = 'ایمیل'
        verbose_name_plural = 'ایمیل'

class NewsLetter(models.Model):
    email = models.EmailField()
    
    class Meta:
        verbose_name = 'خبرنامه'
        verbose_name_plural = 'خبرنامه'


    def __str__(self):
        return self.email


def path_save_blog(instance, filename):
    ext = filename.split('.')[-1]
    filename = f'{instance.title}-{instance.date}.{ext}'
    return f'blog/{filename}'

class Blog(models.Model):
    title = models.CharField(max_length=300, verbose_name='عنوان')
    image = models.ImageField(upload_to=path_save_blog, verbose_name='تصویر')
    description = models.TextField(verbose_name='متن')
    date = models.DateField(auto_now_add=True)

    class Meta:
        verbose_name = 'وبلاگ'
        verbose_name_plural = 'وبلاگ'

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Blog, self).delete()
    
    def save(self, *args, **kwargs):
        try:
            this = Blog.objects.get(id=self.id)
            if this.image != self.image:
                this.image.delete()

        except: 
            pass
        super(Blog, self).save(*args, **kwargs)


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='blog_comment')
    name = models.CharField(max_length=100)
    messages = models.TextField()

    class Meta:
        verbose_name = 'کامنت'
        verbose_name_plural = 'کامنت ها'
        
    def __str__(self):
        return self.name
