from django.contrib import admin

# Register your models here.
from .models import Blog, Comment, Category, Property, Availability, Email, NewsLetter, Images

admin.site.register(Blog)
admin.site.register(Images)
admin.site.register(Email)
admin.site.register(NewsLetter)
admin.site.register(Comment)
admin.site.register(Category)
admin.site.register(Property)
admin.site.register(Availability)