from django.contrib.auth import get_user_model, login, authenticate
from django.core.validators import ip_address_validators
from rest_framework import serializers, status
from django.core.mail import send_mail
from django.shortcuts import redirect
from rest_framework.response import Response
from rest_framework.views import APIView
from property.models import Availability, Blog, Category, Comment, Email, Images, NewsLetter, Property
from accounts.models import Agent
from rest_framework.permissions import IsAdminUser
from rest_framework.pagination import PageNumberPagination
from rest_framework.authtoken.models import Token
from rest_framework.generics import (
                CreateAPIView, GenericAPIView, ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, 
                RetrieveUpdateDestroyAPIView
            )
from .serializers import (
            AgentSerializer, AvailabilitySerializer, CategorySerializer, DetailBlogSerializerAdmin,LogInSerializer,
            CommentSerializer, DetailPropertySerializer, EmailSerializer, ListBlogSerializer, ListPropertySerializer,
            DetailBlogSerializer, ListCASerializer,CreatePropertySerializer, NewsLetterSerializer,DetailPropertySerializerAdmin,
            BlogSerializer, EditEmaigeSerializer,ManageImageSerializer, AddImageSerializer, EmailSendingSerializer
        )


class LogIn(APIView):
    serializer_class = LogInSerializer
    queryset = get_user_model().objects.all()

    def get(self, request):
        srz = self.serializer_class()
        return Response(srz.data, status=status.HTTP_200_OK)
        
    def post(self, request):
        srz = self.serializer_class(data=request.data)

        if srz.is_valid():
            email = srz.data['email']
            password = srz.data['password']

            user = get_user_model().objects.filter(email=email).first()
            user_auth = authenticate(username=user.username, password=password)
            token, created = Token.objects.get_or_create(user=user)
            if user:
                if user.is_active:
                    login(request, user_auth)
                    return redirect('api:index')
                return Response(status=status.HTTP_400_BAD_REQUEST)
            return Response(status=status.HTTP_400_BAD_REQUEST)

        return Response(status=status.HTTP_400_BAD_REQUEST)

class SetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 1000

class SendingEmail(RetrieveAPIView):
    serializer_class = EmailSendingSerializer

    permission_classes = [IsAdminUser]
    
    def get(self, request, *args, **kwargs):
        srz = EmailSendingSerializer()
        return Response(srz.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):

        srz = EmailSendingSerializer(request.data)
        if srz.is_valid():
            emails = NewsLetter.objcets.all()
            subject = srz['subject']
            message = srz['message']
            email_list = [email for email in emails]
            send_mail(
                subject,
                message,
                'Property Site',
                email_list,
                fail_silently=False,
            )
            return Response(srz.data, status=status.HTTP_202_ACCEPTED)
        else:
            srz = NewsLetterSerializer(request.data)
            return Response(srz.errors, status=status.HTTP_400_BAD_REQUEST)

class IndexSite(ListAPIView):
    queryset = Property.objects.all()
    serializer_class = ListPropertySerializer
    pagination_class = SetPagination
    
            
class DetailProperty(RetrieveAPIView):
    
    lookup_field= 'code'
    queryset = Property.objects.all()


    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return DetailPropertySerializerAdmin
        else:
            return DetailPropertySerializer



class BlogList(ListAPIView):
    queryset = Blog.objects.all()
    serializer_class = ListBlogSerializer
    pagination_class = SetPagination
    
class BlogDetail(RetrieveAPIView):
    queryset = Property.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_authenticated and self.request.user.is_admin:
            return DetailBlogSerializerAdmin
        else:
            return DetailBlogSerializer



class UpdateBlog(RetrieveUpdateAPIView):
    queryset = Blog.objects.all()
    serializer_class = BlogSerializer
    permission_classes = [IsAdminUser]

class CreateAgent(CreateAPIView):
    models = Agent
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]

class UpdateAgent(RetrieveUpdateAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]

class CreateCategory(CreateAPIView):
    models = Category
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class UpdateCategory(RetrieveUpdateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminUser]

class UpdateAvail(RetrieveUpdateAPIView):
    queryset = Availability.objects.all()
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAdminUser]

class CreateAvail(CreateAPIView):
    models = Availability
    serializer_class = AvailabilitySerializer
    permission_classes = [IsAdminUser]

class ListCAA(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = ListCASerializer
    permission_classes = [IsAdminUser]

class Agents(ListAPIView):
    queryset = Agent.objects.all()
    serializer_class = AgentSerializer
    permission_classes = [IsAdminUser]

class CreateProperty(CreateAPIView):
    models = Property
    serializer_class = CreatePropertySerializer
    permission_classes = [IsAdminUser]
    
class UpdateProperty(RetrieveUpdateAPIView):
    queryset = Property.objects.all()
    serializer_class = CreatePropertySerializer
    permission_classes = [IsAdminUser]

class CreateEmail(CreateAPIView):
    models = Email
    serializer_class = EmailSerializer

class CreateNewsLetter(CreateAPIView):
    models = NewsLetter
    serializer_class = NewsLetterSerializer

class CreateComment(CreateAPIView):
    models = Comment
    serializer_class = CommentSerializer


class PropertyPiec(ListAPIView):
    serializer_class = ListPropertySerializer
    
    def get_queryset(self):
        name = self.kwargs['name']
        return Property.objects.filter(status = name, is_status_now = 'active')

class EditImages(ListAPIView):
    serializer_class = EditEmaigeSerializer
    permission_classes = [IsAdminUser]
    lookup_field = 'code'

    def get_queryset(self):
        code = self.kwargs['code']
        property = Property.objects.get(code=code)
        images = property.property_image.all()
        return images

class ManageImage(RetrieveUpdateDestroyAPIView):
    queryset = Images.objects.all()
    serializer_class = ManageImageSerializer
    permission_classes = [IsAdminUser]

class AddImages(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request, *args, **kwargs):
        srz = AddImageSerializer()
        return Response(srz.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        property = request.data['property']

        images = dict((request.data).lists())['image']
        
        arr = []
        for image in images:
            data = {'image':image, 'property':property}
            file_serializer = AddImageSerializer(data=data)
            if file_serializer.is_valid():
                file_serializer.save()
                arr.append(file_serializer.data)
            else:
                return Response(arr, status=status.HTTP_400_BAD_REQUEST)

        return Response(arr, status=status.HTTP_201_CREATED)
        
