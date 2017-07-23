import os
from shutil import copy2

from django.db import models
from django.contrib.auth.models import User  # , UserManager

from django.core.validators import RegexValidator
from django_countries.fields import CountryField, Country, countries
from django.db.models.fields.files import FileField, ImageFieldFile, ImageField
# from django.core.files.storage import default_storage
# from django.core.files.base import ContentFile
# from django.conf import settings
# from django.db.models.signals import post_save
# from django.dispatch import receiver

from task2.settings import MEDIA_ROOT


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone_number = models.CharField(validators=[
        RegexValidator(regex=r'^\+?\d{10,15}$', message="Phone number must be entered in the format: '+9999999999'.")],
        max_length=15, blank=True, null=True)
    country = CountryField(blank=True, null=True)
    image = ImageField(upload_to='user/', blank=True, null=True, max_length=255)
    address = models.TextField(max_length=1000, blank=True, null=True)

    def __str__(self):
        return self.user.username

    def __init__(self, *args, **kwargs):
        if kwargs.get('load_from_text'):
            kwargs['image'] = self.make_image_object(str(kwargs.get('image')))
            kwargs['country'] = Country(code=countries.by_name(kwargs.get('country')))
            kwargs.pop('load_from_text')
        super(UserProfile, self).__init__(*args, **kwargs)

    def make_image_object(self, image):
        """makes image object out of provided path if save is called from management command"""

        dest = MEDIA_ROOT + 'user/' + os.path.basename(image)
        head, tail = os.path.splitext(os.path.basename(image))
        count = 0
        while os.path.exists(dest):
            count += 1
            dest = os.path.join(os.path.dirname(dest), '{}-{}{}'.format(head, count, tail))
        copy2(image, dest)
        dest_file = 'user/' + os.path.basename(dest)
        return ImageFieldFile(instance=self, field=FileField(), name=dest_file)


class DateTime(models.Model):
    datetime = models.DateTimeField(blank=True, null=True)
    timezone = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return str(self.datetime)


# Older implementation using Proxy class and post_save signal

# COUNTRY_NAMES = dict([[name, code] for code, name in COUNTRIES.items()])


# class CustomManager(UserManager):
#     def bulk_create(self, items):
#         super(CustomManager, self).bulk_create([i[0] for i in items])
#         for i in items:
#             post_save.send(CustomUser, instance=i[0], created=True, attribs=i[1])
#
#
# class UserProfileManager(models.Manager):
#     def bulk_create(self, items):
#         super(UserProfileManager, self).bulk_create(items)
#
#
# class CustomUser(User):
#     objects = CustomManager()
#
#     class Meta:
#         proxy = True
#         # ordering = ('first_name',)
#
#     def save(self, *args, **kwargs):
#         self._phone_number = kwargs.get('phone_number', None)
#         self._country_name = kwargs.get('country_name', None)
#         self._address = kwargs.get('address', None)
#         self._image = kwargs.get('image', None)
#         kwargs = {}
#         self.full_clean()
#         super(CustomUser, self).save(*args, **kwargs)
#
#
# @receiver(post_save, sender=CustomUser)
# def create_user_profile(sender, instance, created, **kwargs):
#     if 'attribs' in kwargs:
#         phone_number = kwargs.get('attribs').get('phone_number', None)
#         country = kwargs.get('attribs').get('country', None)
#         address = kwargs.get('attribs').get('address', None)
#         image = kwargs.get('attribs').get('image', None)
#     else:
#         phone_number = getattr(instance, '_phone_number', None)
#         country = getattr(instance, '_country_name', None)
#         address = getattr(instance, '_address', None)
#         image = getattr(instance, '_image', None)
#
#     if image:
#         if isinstance(image, str):
#             # from dummy users
#             dest = MEDIA_ROOT + 'user/' + os.path.basename(image)
#             head, tail = os.path.splitext(os.path.basename(image))
#             count = 0
#             while os.path.exists(dest):
#                 count += 1
#                 dest = os.path.join(os.path.dirname(dest), '{}-{}{}'.format(head, count, tail))
#             copy2(image, dest)
#         else:
#             # from browser
#             path = default_storage.save('user/' + image.name, ContentFile(image.read()))
#             dest = os.path.join(settings.MEDIA_ROOT, path)
#         dest_file = 'user/' + os.path.basename(dest)
#         image = ImageFieldFile(instance=instance, field=FileField(), name=dest_file)
#     if country:
#         country = Country(code=country if country in COUNTRIES else COUNTRY_NAMES[country])
#
#     if created:
#         UserProfile.objects.create(user=instance, phone_number=phone_number,
#                                    country=country, address=address, image=image)
