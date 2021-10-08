from django.conf import settings
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model

class Command(BaseCommand):

    def handle(self, *args, **options):
        if get_user_model().objects.count() == 0:
            username = 'admin'
            email = 'admin@gmail.com'
            password = 'admin'
            admin = get_user_model().objects.create_superuser(username=username, email=email, password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin accounts can only be initialized if no Accounts exist')