from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext_lazy as _
from .forms import RegisterForm, LoginForm
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login,logout,authenticate



def signup(request):
    if request.user.is_authenticated:
        return redirect('accounts:signout')

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            get_user_model().objects.create_user(username = cd['username'], email=cd['email'], password = cd['password'])
            messages.success(request,_('your submited is successfully'),'success')
            return redirect('acounts:sigin')
        else:
            form = RegisterForm(request.POST)
            messages.warning(request, _('please check fields'),'warning')
            return render(request, 'register.html',{'form':form, 'label':'ایجاد اکانت'})
    else:
        form = RegisterForm()
        return render(request, 'register.html', {'form':form, 'label':'ایجاد اکانت'})

def signin(request):
    if request.user.is_authenticated:
        return redirect('accounts:signout')

    if request.method == 'POST':
        data = {'email':request.POST.get('email'), 'password':request.POST.get('password')}
        form = LoginForm(request.POST or None,data)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['email']:
                user = get_user_model().objects.filter(email = cd['email']).first()
                if not user:
                    messages.warning(request, _('please check username or email'), 'error')
                    return render(request, 'register.html',{'form':form, 'label':'ورود به سایت'})


            user_auth = authenticate(username = user.username, password = cd['password'])
            login(request,user_auth)
            messages.success(request, _('your login to site successfull'),'success')
            return redirect('property:index')

        else:
            form = LoginForm(request.POST)
            messages.warning(request, _('please check fields'),'warning')
            return render(request, 'register.html', {'form':form, 'label':'ورود به سایت'})
    else:
        form = LoginForm()
        return render(request, 'register.html', {'form':form, 'label':'ورود به سایت'})


@login_required
def signout(request):
    logout(request)
    messages.success(request, 'شما از سایت خارج شدید', 'success')
    return redirect('property:index')