from django.contrib import admin
from .models import User, Agent
from .forms import UserChangeForm, UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

admin.site.register(Agent)

@admin.register(User)
class AdminUser(BaseUserAdmin):

    form = UserChangeForm
    add_form = UserCreationForm
    list_display = ('username', 'email', 'is_admin', 'is_active')
    list_filter = ('is_admin', )

    fieldsets = ( #this is for form
        ('اطلاعات شخصی',{'fields':('username','email','password')}),
        ('دسترسی',{'fields':('is_active','is_admin')}),
        ('محدودیت',{'fields':('groups', 'user_permissions')}),
    )
    add_fieldsets = (#this is for add_form 
        ( 'اطلاعات شخصی',{'fields':('username', 'email', 'password','password_confierm')}),
        ('دسترسی',{'fields':('is_active','is_admin', 'groups', 'user_permissions')})
    )

    search_fields = ('username',)
    ordering = ('username',)
    filter_horizontal = ()

    actions = ('make_admin',)

    def make_admin(self, request, queryset):
        queryset.update(is_admin=True)