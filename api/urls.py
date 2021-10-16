from django.urls import path

from property.models import Property
from .views import (
        IndexSite, DetailProperty, BlogList, BlogDetail, CreateNewsLetter,
        CreateAgent, UpdateAgent, CreateCategory, UpdateCategory,CreateEmail,
        CreateAvail, UpdateAvail, ListCAA,Agents,CreateProperty,UpdateProperty,
        CreateComment,PropertyPiec,CreateComment,PropertyPiec,UpdateBlog,
        EditImages,ManageImage,AddImages, SendingEmail
    )
app_name = 'api'

urlpatterns = [ 
    path('', IndexSite.as_view(), name='index'),
    path('list/CatAval/', ListCAA.as_view(), name='list'),
    path('blogs/', BlogList.as_view(), name='index'),
    path('sending/email/', SendingEmail.as_view(), name='email_sending'),
    path('blogs/detail/<int:pk>/', BlogDetail.as_view(), name='blog_detail'),
    path('detail/<str:code>/', DetailProperty.as_view(), name='detail'),
    path('create/agent/', CreateAgent.as_view(), name='create_agent'),
    path('update/agent/<int:pk>/', UpdateAgent.as_view(), name='update_agent'),
    path('create/category/', CreateCategory.as_view(), name='create_category'),
    path('update/category/<int:pk>/', UpdateCategory.as_view(), name='update_category'),
    path('create/avail/', CreateAvail.as_view(), name='create_avail'),
    path('update/avail/<int:pk>/', UpdateAvail.as_view(), name='update_avail'),
    path('agents/', Agents.as_view(), name='agents'),
    path('create/email/', CreateEmail.as_view(), name='create_Email'),
    path('create/newsletter/', CreateNewsLetter.as_view(), name='create_newsletter'),
    path('create/comment/', CreateComment.as_view(), name='create_comment'),
    path('property/<str:name>/', PropertyPiec.as_view(), name='property_piec'),    
    path('edit/images/<str:code>/', EditImages.as_view(), name='edit_images'),
    path('add/images/', AddImages.as_view(), name='add_images'),
    path('manage/emaige/<int:pk>/', ManageImage.as_view(), name='manage_image'),

    path('create/property/', CreateProperty.as_view(), name='create_property'),
    path('update/property/<int:pk>/', UpdateProperty.as_view(), name='update_property'),
    path('update/blog/<int:pk>/', UpdateBlog.as_view(), name='update_blog'),

]   