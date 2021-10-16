from django import forms
from django.contrib.gis.geos import  Point
from location_field.models.spatial import LocationField
from .models import Blog, Images, Property, Email, NewsLetter, Comment


messages = {
    'required':"این فیلد الزامیست",
    'max_length':"تعداد کاراکتر را کاهش دهید",
    'min_length':"تعداد کاراکتر را افزایش دهید",
    'max_value':"اعداد را کاهش دهید",
    'min_value':"اعداد را افزایش دهید ",
    'invalid':'این فیلد صحیحی نمیباشد'
}
from location_field.forms.spatial import LocationField
#from location_field.models.spatial import LocationField ---> for using spatil Database like postgis
#from location_field.forms.spatial import LocationField ---> for using spatil Database like postgis
#from location_field.models.plain import PlainLocationField ---> for usage without Database
#from location_field.forms.plain import PlainLocationField ---> for usage without Database


class PropertyForm(forms.ModelForm):
    location = LocationField(based_fields=['city'])

    rating = forms.IntegerField(
        min_value=0,
        max_value=10,
        error_messages=messages,
        widget=forms.TextInput(attrs={'class':'form-control', 'placeholder':'امتیاز از 10...'})
    )

    def __init__(self,*args, **kwargs):
        super(PropertyForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model=Property
        fields = ('name','category','availability','agent','address','description','price','title','image','rating','status','is_status_now', 'location')

        widgets ={
            'name':forms.TextInput(attrs={'placeholder':"نام ..."}),
            'address':forms.TextInput(attrs={'placeholder':" آدرس ..."}),
            'description':forms.TextInput(attrs={'placeholder':" توضیحات ..."}),
            'price':forms.TextInput(attrs={'placeholder':" قیمت ..."}),
            'title':forms.TextInput(attrs={'placeholder':" عنوان ..."}),
            'rating':forms.TextInput(attrs={'placeholder':" امتیاز ..."}),
        }

class EmailForm(forms.ModelForm):
    code = forms.CharField(
        widget = forms.HiddenInput(attrs={'readonly':'readonly', 'hidden':'hidden'})
    )

    def __init__(self,*args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model = Email
        fields = ('code','full_name','email','phone','message')
    
        widgets ={
            'email':forms.TextInput(attrs={'placeholder':"ایمیل شما ..."}),
            'full_name':forms.TextInput(attrs={'placeholder':"نام شما ..."}),
            'phone':forms.TextInput(attrs={'placeholder':"تلفن شما ..."}),
            'message':forms.TextInput(attrs={'placeholder':"پیغام شما ..."}),

        }

class CommentForm(forms.ModelForm):
    blog = forms.IntegerField(
        widget = forms.HiddenInput(attrs={'readonly':'readonly', 'hidden':'hidden'})
    )
    def __init__(self,*args, **kwargs):
        super(CommentForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model = Comment
        fields = ('blog', 'name', 'messages')
    
        widgets ={
            'name':forms.TextInput(attrs={'placeholder':"نام شما ..."}),
            'messages':forms.Textarea(attrs={'placeholder':"پیغام شما ..."}),

        }
class CommentSave(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('blog', 'name', 'messages')
    
class BlogForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(BlogForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model=Blog
        fields = ('title','image','description')
    
        widgets ={
            'title':forms.TextInput(attrs={'placeholder':" عنوان ..."}),
            'description':forms.Textarea(attrs={'placeholder':" توضیحات ..."}),
        }

class NewsletterForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(NewsletterForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model=NewsLetter
        fields = ('email',)

        widgets ={
            'email':forms.TextInput(attrs={'placeholder':"ایمیل شما ..."}),
            }

class EmalSendingForm(forms.Form):
    subject = forms.CharField(
        error_messages=messages,
        label= 'موضوع',
        widget = forms.TextInput(attrs={'class':'form-control', 'placeholder':'موضوع...'})
    )
    message = forms.CharField(
        error_messages=messages,
        label= 'پیغام',
        widget = forms.Textarea(attrs={'class':'form-control', 'placeholder':'پیغام شما...'})
    )

class AddImagesForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AddImageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].widget.attrs['multiple']='multiple'
            self.fields[field].error_messages = messages

    class Meta:
        model = Images
        fields = ('image',)

class AddImageForm(forms.ModelForm):
    def __init__(self,*args, **kwargs):
        super(AddImageForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class']='form-control'
            self.fields[field].error_messages = messages

    class Meta:
        model = Images
        fields = ('image',)
