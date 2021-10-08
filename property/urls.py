from django.urls import path
from .views import (
            create_property, email_submit,edit_property, 
            index,about,blog,property_detail,contact,
            agent, email_sending,search,blog_single,
            create_blog,edit_blog,save_news_letter,
            add_image,create_comment
        )

app_name = 'property'

urlpatterns = [
    path('', index, name="index"),
    path('about/', about, name="about"),
    path('blog/', blog, name="blog"),
    path('property/detail/<str:code>/', property_detail, name="property_detail"),
    path('contact/', contact, name="contact"),
    path('agent/', agent, name="agent"),
    path('search/<str:name>/', search, name="search"),
    path('create/', create_property, name="create_property"),
    path('create/blog/', create_blog, name="create_blog"),
    path('edit/<str:code>/', edit_property, name="edit_property"),
    path('add/image/<str:code>/', add_image, name="add_image"),
    path('blog/single/<int:pk>/', blog_single, name="blog_single"),
    path('edit/blog/<int:pk>/', edit_blog, name="edit_blog"),
    path('email/submit/', email_submit, name="email_submit"),
    path('email/sending/', email_sending, name="email_sending"),
    path('news/letter/', save_news_letter, name="save_news_letter"),
    path('create/comment/', create_comment, name="create_comment"),
]