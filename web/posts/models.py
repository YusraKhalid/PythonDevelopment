from django.db import models
from django.utils import timezone
from web.users.models import Address


class Post(models.Model):
    posted_by = models.ForeignKey('users.User', related_name='posts')
    title = models.CharField(max_length=255)
    area = models.DecimalField(decimal_places=3, max_digits=100)
    location = models.OneToOneField(Address)
    description = models.CharField(max_length=1024)
    kind = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=255)
    demanded_price = models.DecimalField(decimal_places=3, max_digits=100)
    is_sold = models.BooleanField(default=False)
    sold_on = models.DateTimeField(default=timezone.now)
    posted_on = models.DateTimeField(default=timezone.now)
    expired_on = models.DateTimeField()
    is_expired = models.BooleanField(default=False)

    @property
    def get_number_of_views(self):
        return self.post_views.all().count()

    @property
    def is_post_expired(self):
        if not self.is_expired:
            time_delta = self.expired_on - timezone.now()
            if time_delta.total_seconds() < 0:
                self.is_expired = True
                self.save()
        return self.is_expired

    @property
    def time_until_expired(self):
        days_hours_minutes_dict = None
        time_delta = self.expired_on - timezone.now()
        days, hours, minutes = time_delta.days, time_delta.seconds // 3600, time_delta.seconds // 60 % 60
        if days > 0:
            days_hours_minutes_dict = dict(days=days, hours=hours, minutes=minutes)
        return days_hours_minutes_dict

    def reactivate_post(self, days):
        self.is_expired = False
        self.expired_on = timezone.now() + timezone.timedelta(days=days)
        self.save()


class Picture(models.Model):
    post = models.ForeignKey('Post', related_name='pictures')
    url = models.CharField(max_length=1024)
    is_expired = models.BooleanField(default=False)


class Request(models.Model):
    requested_by = models.ForeignKey('users.User', related_name='requests')
    post = models.ForeignKey('Post', related_name='requests')
    message = models.CharField(max_length=512)
    price = models.DecimalField(decimal_places=3, max_digits=100)
    status = models.CharField(max_length=255, default='pending')
    requested_on = models.DateTimeField(default=timezone.now)


class PostView(models.Model):
    viewed_by = models.ForeignKey('users.User', related_name='views')
    post_viewed = models.ForeignKey('posts.Post', related_name='post_views')
    viewed_on = models.DateTimeField(default=timezone.now)





