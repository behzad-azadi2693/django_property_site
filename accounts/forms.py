from django import forms
from .models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField


messages = {
    'required':"این فیلد الزامیست",
    'max_length':"تعداد کاراکتر را کاهش دهید",
    'min_length':"تعداد کاراکتر را افزایش دهید",
    'max_value':"اعداد را کاهش دهید",
    'min_value':"اعداد را افزایش دهید ",
    'invalid':'این فیلد صحیح نمیباشد'
}

class UserCreationForm(forms.ModelForm):
    password = forms.CharField(label='password', widget=forms.PasswordInput)
    password_confierm = forms.CharField(label='password_confierm', widget=forms.PasswordInput)

    class Meta:
        models = User
        fields = ('username', 'email', 'password', 'password_confierm')

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError("پسورد و تکرار یکی باشند")

        return cd['password_confierm']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user
class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()
    class Meta:
        models = User
        fields = ('username', 'email', 'password')

    def clean_password(self):
        return self.initial['password']

class RegisterForm(forms.Form):
    username = forms.CharField(label='username', widget=forms.TextInput,min_length=4)
    email = forms.EmailField(label='email', widget=forms.EmailInput,)
    password = forms.CharField(label='password', widget=forms.PasswordInput,min_length=4)
    password_confierm = forms.CharField(label='password_confierm', widget=forms.PasswordInput, min_length=4)

    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'contact_input'
            self.fields[field].error_messages = messages

    
    def clean_username(self):
        cd = self.cleaned_data['username']
        user = User.objects.filter(username = cd).first()
        if user:
            raise forms.ValidationError('this username is exits')
        return cd

    def clean_email(self):
        cd = self.cleaned_data['email']
        user = User.objects.filter(email = cd).first()
        if user:
            raise forms.ValidationError('این ایمیل مجاز نمیباشد')
        return cd

    def clean_password_confierm(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password_confierm'] and cd['password'] != cd['password_confierm']:
            raise forms.ValidationError("پسورد و تکرار یکی باشند ")
        
        return cd['password_confierm']


class LoginForm(forms.Form):
    email = forms.EmailField(label='email', widget=forms.EmailInput(attrs={'placeholder':'email'}),required=False)
    password = forms.CharField(label='password', widget=forms.PasswordInput(attrs={'placeholder':'password'}),min_length=4)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)

        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            self.fields[field].error_messages = messages

    def clean_email(self):
        cd = self.cleaned_data
        email_cd = cd['email']
        email = User.objects.filter(email=email_cd).first()

        if not email:
            raise forms.ValidationError('لطفا ایمیل را وارد کنید')
        return email_cd

