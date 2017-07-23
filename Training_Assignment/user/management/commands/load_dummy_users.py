import csv
import datetime
from pytz import timezone

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.core.cache import cache

from user.models import UserProfile, DateTime



class Command(BaseCommand):
    def handle(self, **options):
        count = cache.set('count', 0)
        convert = cache.set('convert', True)
        dt = datetime.datetime.now()
        tz = timezone('Asia/Karachi')
        dtz = tz.normalize(tz.localize(dt))
        datetime_list = []
        for i in range(100):
            datetime_list.append(DateTime(datetime=dtz, timezone=tz.zone))
        DateTime.objects.bulk_create(datetime_list)
        with open('dummy.csv', 'r') as csvfile:
            users_info = csv.DictReader(csvfile)
            users = []

            for user in users_info:
                users.append(UserProfile(
                    user=User.objects.create(username='{}.{}'.format(user['first_name'], user['last_name']),
                                             password=make_password(user['password']), first_name=user['first_name'],
                                             last_name=user['last_name']), phone_number=user['phone_number'],
                    country=user['country'], address=user['address'], image=user['image'], load_from_text=True))
            UserProfile.objects.bulk_create(users)

            # for user in users_info:
            #     dummy_user = CustomUser(username='{}.{}'.format(user['first_name'], user['last_name']),
            #                             password=make_password(user['password']), email=user['email'],
            #                             first_name=user['first_name'], first_name=user['first_name'])
            #     users.append([dummy_user, {'phone_number': user['phone_number'], 'image': user['image'],
            #                                'country': user['country'], 'address': user['address']}])
            # CustomUser.objects.bulk_create(users)
