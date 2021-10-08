from django.http.response import Http404
from django.shortcuts import redirect, render, get_object_or_404
from .models import Availability, Blog, Category, Comment, Email, Property
from accounts.models import Agent
from django.contrib.auth.decorators import login_required 
from .forms import (
                AddImageForm, CommentForm, NewsletterForm,
                EmailForm, PropertyForm, EmalSendingForm,
                BlogForm, CommentSave,
            )
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
import redis

conn = redis.Redis('redis_container', port= 6379, db=0,password="admin", charset='utf-8', decode_responses=True) 
#decode_response for convert b'one':b'1' to 'one':'1'


def index(request):
    properties = Property.objects.filter(rating__gte = 7)[:8]
    
    context = {
        'properties':properties,
    }

    return render(request, 'index.html', context)


def about(request):
    return render(request, 'about.html')


from django.db.models import Count

def blog(request):
    blogs = Blog.objects.all()
    recents = Blog.objects.all().order_by('-id')[:3]

    o_list = Comment.objects.values('blog_id').annotate(ocount=Count('blog_id'))
    top_three_ojcect = sorted(o_list, key = lambda k: k['ocount'])[:3]
    list_pk = [obj['blog_id'] for obj in top_three_ojcect]
    mosts = Blog.objects.filter(pk__in = list_pk)

    context = {
        'blogs':blogs,
        'recents':recents,
        'mosts':mosts
    }

    return render(request, 'blog.html', context)

def blog_single(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    recents = Blog.objects.all().order_by('-id')[:3]

    ip = request.META.get('remote_addr')
    key = f'blog_view:{blog.pk}'
    conn.sadd(key, ip)
    count_number = conn.scard(key)

    o_list = Comment.objects.values('blog_id').annotate(ocount=Count('blog_id'))
    top_three_ojcect = sorted(o_list, key = lambda k: k['ocount'])[:3]
    list_pk = [obj['blog_id'] for obj in top_three_ojcect]
    mosts = Blog.objects.filter(pk__in = list_pk)
    data = {'blog':blog.pk}
    context = {
        'blog':blog,
        'recents':recents,
        'mosts':mosts,
        'form':CommentForm(initial=data),
        'count_number':count_number
    }

    return render(request, 'blogdetail.html', context)

@login_required
def create_blog(request):
    if not request.user.is_admin:
        return Http404('this page not valid')

    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect('property:blog_single', obj.pk)
        else:
            form = BlogForm(request.POST, request.FILES)
            return render(request, 'register.html', {'form':form, 'label':'create blog'})
    else:
        form = BlogForm()
        return render(request, 'register.html', {'form':form, 'label':'create blog'})


@login_required
def edit_blog(request, pk):
    if not request.user.admin:
        return Http404('this page not valid')

    obj = get_object_or_404(Blog, pk=pk)
    if request.method == 'POST':
        form = BlogForm(request.POST, request.FILES, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('property:blog_single', obj.pk)
        else:
            form = BlogForm(request.POST, request.FILES, instance=obj)
            return render(request, 'blogdetail.html', {'form':form, 'label':'create blog'})
    else:
        form = BlogForm(instance=obj)
        return render(request, 'blogdetail.html', {'form':form, 'label':'create blog'})


def property_detail(request, code):
    property = get_object_or_404(Property, code=code)
    properties = Property.objects.filter(category = property.category).order_by('?')[:4]
    avas = Availability.objects.filter(property_avail = property)
    
    key = f'property_view:{property.pk}'
    if property.is_status_now == 'active':
        ip = request.META.get('REMOTE_ADDR')
        conn.sadd(key, ip)
    count_number = conn.scard(key)

    data = {'code':property.code}
    form = EmailForm(initial = data)
    context={
        'properties':properties,
        'property':property,
        'form':form,
        'avas':avas,
        'count_number': count_number
    }
    return render(request, 'property-detail.html', context)

def contact(request):
    return render(request, 'contact.html')


def agent(request):
    agents = Agent.objects.all()
    context = {
        'agents':agents
    }
    return render(request, 'agents.html', context)

@login_required
def create_property(request):
    if not request.user.is_admin:
        return Http404('path not valid')

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save()
            return redirect('property:property_detail', obj.code)
        else:
            form = PropertyForm(request.POST, request.FILES)
            return render(request,'register.html', {'form':form, 'label':'ایجاد ملک جدید'})
    else:
        form = PropertyForm()
        return render(request,'register.html', {'form':form, 'label':'ایجاد ملک جدید'})

@login_required
def edit_property(request, code):
    if not request.user.is_admin:
        return Http404('path not valid')

    property = get_object_or_404(Property, code=code)

    if request.method == 'POST':
        form = PropertyForm(request.POST, request.FILES, instance=property)
        if form.is_valid():
            obj = form.save()
            return redirect('property:property_detail', obj.code)
        else:
            form = PropertyForm(request.POST, request.FILES, instance=property)
            return render(request,'register.html', {'form':form, 'label':'ویرایش اطلاعات'})
    else:
        form = PropertyForm(instance=property)
        return render(request,'register.html', {'form':form, 'label':'ویرایش اطلاعات'})

def save_news_letter(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            messages.warning(request, 'ایمیل شما با موفقیت ثبت نشد لطفا مجدد اقدام نمایید', 'warning')
            return redirect('property:index')
        data = {'email':email}
        form = NewsletterForm(request.POST or None, data)
        if form.is_valid():
            form.save()
            messages.success(request, 'ایمیل شما با موفقیت ثبت شد', 'success')
            return redirect('property:index')
        else:
            messages.warning(request, 'ایمیل شما با موفقیت ثبت نشد لطفا مجدد اقدام نمایید', 'warning')
            return redirect('property:index')
    else:
        return redirect('property:index')


def email_submit(request):
    if request.method == 'POST':
        form = EmailForm(request.POST)
        if form.is_valid():
            obj = form.save()
            subject = f'{obj.full_name}-{obj.phone}'
            message = obj.message
            send_mail(
                subject,
                message,
                'Property Site',
                'admin@gmail.com',
                fail_silently=False,
            )
            messages.success(request, 'ایمیل شما با موفقیت برای ادمین ارسال شد', 'success')
            return redirect('property:propety_detail', obj.code)
        else:
            code = request.POST['code']
            messages.warning(request, 'ایمیل شما با موفقیت برای ادمین ارسال شد', 'error')
            return redirect('property:propety_detail', code)

    else:
        return Http404('this path not valid')

@login_required
def email_sending(request):
    if not request.user.is_admin:
        return Http404('this path is not valid')

    if request.method == 'POST':
        form = EmalSendingForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            emails = NewsletterForm.objcets.all()

            subject = cd['subject']
            message = cd['message']
            email_list = [email for email in emails]
            send_mail(
                subject,
                message,
                'Property Site',
                email_list,
                fail_silently=False,
            )
            messages.success(request, 'ایمیل ارسال شد', 'success')
            return redirect('property:email_sending')
        else:
            form = EmalSendingForm(request.POST)
            return render(request, 'register.html',{'form':form, 'label':'ارسال ایمیل'})
    else:
        form = EmalSendingForm()
        return render(request, 'register.html',{'form':form, 'label':'ارسال ایمیل'})


def search(request, name=None):
    
    if name is not None:
        properties = Property.objects.filter(status = name)
        hots = Property.objects.filter(status = name).order_by('-price')[:4]
    else:
        properties = Property.objects.all()
        hots = Property.objects.order_by('-price')[:4]


    if request.method == 'GET':
        if request.GET.get('text'):
            name = request.GET.get('text')
            properties = properties.filter(description__contains=name)

        if request.GET.get('status'):
            name = request.GET.get('status')
            properties = properties.filter(status = name)
            hots = Property.objects.filter(status = name).order_by('-price')[:4]

        if request.GET.get('price'):
            name = request.GET.get('price')
            properties = properties.filter(price__lte = name)
        
        if request.GET.get('category'):
            name = request.GET.get('category')
            properties = properties.filter(category__name = name)
    
    page = request.GET.get('page', 1)

    paginator = Paginator(properties, 12)

    try:
        searchs = paginator.page(page)
    except PageNotAnInteger:
        searchs = paginator.page(1)
    except EmptyPage:
        searchs = paginator.page(paginator.num_pages)


    context = {
        'hots':hots,
        'properties':properties,
        'searchs' : searchs,
        'status':request.GET.get('status'),
        'price':request.GET.get('price'),
        'category':request.GET.get('category'),
        'text':request.GET.get('text'),
        'my_count':  ((searchs.number - 1) * 12 + (properties.count() - (searchs.number - 1) * 12 ))
    }

    return render(request, 'buysalerent.html', context )


@login_required
def add_image(request, code):
    if not request.user.is_admin:
        return Http404('this path is not valid')

    property = get_object_or_404(Property, code=code)

    if request.method == 'POST':
        form = AddImageForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.property = property
            obj.save()
            return redirect('property:property_detail', property.code)
        else:
            return render(request, 'register.html', {'form':form, 'label':'add image'})
    else:
        form = AddImageForm()
        return render(request, 'register.html', {'form':form, 'label':'add image'})


def create_comment(request):
    pk = request.POST.get('blog')
    blog = get_object_or_404(Blog, pk=pk)
    
    if request.method == 'POST':
        data = {'blog':blog}
        form = CommentSave(request.POST, instance=blog)
        if form.is_valid():
            form.cleaned_data
            form.save()
            messages.success(request, 'نظر شما با موفقیت ثبت شد', 'success')
            return redirect('property:blog_single', blog.pk)
        else:
            messages.warning(request, 'نظر شما با موفقیت ثبت نشد مجدد اقدام نمایید', 'warning')
            return redirect('property:blog_single', blog.pk)
    else:
        messages.warning(request, 'نظر شما با موفقیت ثبت نشد مجدد اقدام نمایید', 'warning')
        return redirect('property:blog_single', blog.pk)