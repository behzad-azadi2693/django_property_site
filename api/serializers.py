from rest_framework import serializers
from rest_framework.serializers import HyperlinkedIdentityField, ModelSerializer, SerializerMetaclass, SerializerMethodField
from accounts.models import Agent
from property.models import Blog, Category, Email, Images, NewsLetter, Property, Comment, Availability
from rest_framework.reverse import reverse
from django.db.models import Count, fields
from django.contrib.auth import get_user_model
import redis
conn = redis.Redis('redis_container', port= 6379, db=0,password="admin", charset='utf-8', decode_responses=True) 

class EmailSendingSerializer(serializers.Serializer):
    subject = serializers.CharField(allow_blank=True,max_length=200)
    message = serializers.CharField(allow_blank=True,style={'base_template': 'textarea.html'})
    
class AvailabilitySerializer(ModelSerializer):
    class Meta:
        model = Availability
        fields = ('name',)

class AgentSerializer(ModelSerializer):
    class Meta:
        model = Agent
        exclude = ('id',)

class LogInSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()
    
class CategorySerializer(ModelSerializer):
    class Meta:
        model = Category
        fields = ('name',)

class ListPropertySerializer(ModelSerializer):
    availability = AvailabilitySerializer(many=True, read_only=True)
    url_detail = HyperlinkedIdentityField(view_name='api:detail',lookup_field = 'code',lookup_url_kwarg = 'code')

    class Meta:
        model = Property
        fields = ('name','availability','price','image','is_status_now', 'url_detail')

class MinyPropertySerializer(ModelSerializer):
    url_detail = SerializerMethodField()

    class Meta:
        model = Property
        fields = ('name','price','image','url_detail')
    
    def get_url_detail(self, obj):
        return obj.get_api_url()

class ImagesSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ('image',)

class AddImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        exclude = ('id',)

class CreatePropertySerializer(ModelSerializer):
    
    class Meta:
        model = Property
        fields = (
            'name','code','category','availability','agent','address','description',
            'price','title','image','rating','status','is_status_now','date','location'
        )

class DetailPropertySerializer(ModelSerializer):
    availability = AvailabilitySerializer(many=True, read_only=True)
    images = SerializerMethodField()
    category = CategorySerializer()
    agent = AgentSerializer()
    category_property = SerializerMethodField()
    count_number = SerializerMethodField()

    class Meta:
        model = Property
        fields = (
            'count_number','name','code','category','availability','agent','address','description',
            'price','title','image','rating','status','is_status_now','date','location','images',
            'category_property'
        )
        
    def get_images(self, obj):
        images = Images.objects.filter(property = obj)
        all_image = ImagesSerializer(images, many=True).data 
        return all_image

    def get_category_property(self, obj):
        prts = Property.objects.filter(category = obj.category)
        result = MinyPropertySerializer(prts, many=True).data
        return result

    def get_count_number(self, obj):
        key = f'property_view:{obj.pk}'
        number = conn.scard(key)
        return number

    
class DetailPropertySerializerAdmin(ModelSerializer):
    edit_images = HyperlinkedIdentityField(view_name='api:edit_images',lookup_field = 'code', lookup_url_kwarg = 'code')
    add_images = HyperlinkedIdentityField(view_name='api:add_images', lookup_field = 'code', lookup_url_kwarg = 'code')
    url_update = HyperlinkedIdentityField(view_name='api:update_property')
    availability = AvailabilitySerializer(many=True, read_only=True)
    images = SerializerMethodField()
    category = CategorySerializer()
    agent = AgentSerializer()
    count_number = SerializerMethodField()
    category_property = SerializerMethodField()
    
    class Meta:
        model = Property
        fields = (
            'count_number','url_update','pk','edit_images','add_images','name','code','category','availability','agent','address',
            'description','price','title','image','rating','status','is_status_now','date','location',
            'images','category_property'
        )

    def get_count_number(self, obj):
        key = f'property_view:{obj.pk}'
        number = conn.scard(key)
        return number
    
    def get_images(self, obj):
        images = Images.objects.filter(property = obj)
        all_image = ImagesSerializer(images, many=True).data 
        return all_image

    def get_category_property(self, obj):
        prts = Property.objects.filter(category = obj.category)
        result = MinyPropertySerializer(prts, many=True).data
        return result

    #def get_url_update(self, obj):
    #    result = '{}'.format(reverse('update_property', args=[obj.id]))
    #    return result

class ListBlogSerializer(ModelSerializer):
    url_blog = SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('image','title', 'url_blog')

    def get_url_blog(self, obj):
        return obj.get_api_url()

class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        fields = ('name', 'messages')


class DetailBlogSerializer(ModelSerializer):
    comments = SerializerMethodField()
    most_comment = SerializerMethodField()
    recent_blog = SerializerMethodField()
    comment = CommentSerializer(write_only=True)
    count_number = SerializerMethodField()

    class Meta:
        model = Blog
        fields = ('count_number','image','title','description','date', 'comments', 'most_comment', 'recent_blog', 'comment')

    def get_count_number(self, obj):
        key = f'blog_view:{obj.pk}'
        number = conn.scard(key)
        return number

    def get_comments(self, obj):
        cmt = Comment.objects.filter(blog=obj)
        all_cmt = CommentSerializer(cmt, many=True).data
        return all_cmt

    def get_most_comment(self, obj):
        o_list = Comment.objects.values('blog_id').annotate(ocount=Count('blog_id'))
        top_three_ojcect = sorted(o_list, key = lambda k: k['ocount'])[:3]
        list_pk = [obj['blog_id'] for obj in top_three_ojcect]
        mosts = Blog.objects.filter(pk__in = list_pk)

        result = ListBlogSerializer(mosts, many=True).data 
        return result

    def get_recent_blog(self, obj):
        recents = Blog.objects.all().order_by('-id')[:3]
        result = ListBlogSerializer(recents, many=True).data 
        return result

class BlogSerializer(ModelSerializer):
    class Meta:
        model = Blog
        fields = ('image','title','description')


class DetailBlogSerializerAdmin(ModelSerializer):
    url_update = HyperlinkedIdentityField(view_name='api:update_blog')
    comments = SerializerMethodField()
    most_comment = SerializerMethodField()
    recent_blog = SerializerMethodField()
    comment = CommentSerializer(write_only=True)
    count_number = SerializerMethodField()
    class Meta:
        model = Blog
        fields = ('count_number','url_update','image','title','description','date', 'comments', 'most_comment', 'recent_blog', 'comment')
    
    def get_count_number(self, obj):
        key = f'blog_view:{obj.pk}'
        number = conn.scard(key)
        return number

    def get_comments(self, obj):
        cmt = Comment.objects.filter(blog=obj)
        all_cmt = CommentSerializer(cmt, many=True).data
        return all_cmt

    def get_most_comment(self, obj):
        o_list = Comment.objects.values('blog_id').annotate(ocount=Count('blog_id'))
        top_three_ojcect = sorted(o_list, key = lambda k: k['ocount'])[:3]
        list_pk = [obj['blog_id'] for obj in top_three_ojcect]
        mosts = Blog.objects.filter(pk__in = list_pk)

        result = ListBlogSerializer(mosts, many=True).data 
        return result

    def get_recent_blog(self, obj):
        recents = Blog.objects.all().order_by('-id')[:3]
        result = ListBlogSerializer(recents, many=True).data 
        return result
    
class CatSerializer(ModelSerializer):
    url_update = SerializerMethodField()

    class Meta:
        model = Category
        fields = ('name', 'url_update')

    def get_url_update(self, obj):
        result = '{}'.format(reverse('api:update_category', args=[obj.pk]))
        return result

class AvalSerializer(ModelSerializer):
    url_update = SerializerMethodField()

    class Meta:
        model = Availability
        fields = ('name', 'url_update')

    def get_url_update(self, obj):
        result = '{}'.format(reverse('api:update_avail', args=[obj.pk]))
        return result

class AgesSerializer(ModelSerializer):
    url_update = SerializerMethodField()

    class Meta:
        model = Agent
        exclude = ('id',)

    def get_url_update(self, obj):
        result = '{}'.format(reverse('api:update_agent', args=[obj.pk]))
        return result

class ListCASerializer(ModelSerializer):
    create_property = SerializerMethodField()
    create_category = SerializerMethodField()
    create_available = SerializerMethodField()
    create_agent = SerializerMethodField()
    agent = SerializerMethodField()
    category = SerializerMethodField()
    availability = SerializerMethodField()
    
    class Meta:
        model = Category
        fields = ('create_property','create_category','create_available', 'create_agent','category', 'availability', 'agent')
    
    def get_create_category(self, obj):
        result = '{}'.format(reverse('api:create_category'))
        return result
    
    def get_create_property(self, obj):
        result = '{}'.format(reverse('api:create_property'))
        return result
    
    def get_create_available(self, obj):
        result = '{}'.format(reverse('api:create_avail'))
        return result

    def get_create_agent(self, obj):
        result = '{}'.format(reverse('api:create_agent'))
        return result

    def get_category(self, obj):
        cats = Category.objects.all()
        result = CatSerializer(cats, many=True).data
        return result

    def get_availability(self, obj):
        avals = Availability.objects.all()
        result = AvalSerializer(avals, many=True).data
        return result

    def get_agent(self, obj):
        ags = Agent.objects.all()
        result = AgesSerializer(ags, many=True).data 
        return result

class EmailSerializer(ModelSerializer):
    class Meta:
        model = Email
        exclude = ('id',)

class NewsLetterSerializer(ModelSerializer):
    class Meta:
        model = NewsLetter
        exclude = ('id',)
    
class CommentSerializer(ModelSerializer):
    class Meta:
        model = Comment
        exclude = ('id',)


class EditEmaigeSerializer(ModelSerializer):
    manage_image = HyperlinkedIdentityField(view_name='api:manage_image')

    class Meta:
        model = Images
        fields = ('image', 'manage_image')

class ManageImageSerializer(ModelSerializer):
    class Meta:
        model = Images
        fields = ('image',)