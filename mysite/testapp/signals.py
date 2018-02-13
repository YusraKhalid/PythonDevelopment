from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def generate_token(sender, instance, **kwargs):
	token = None
	try:
		token = instance.auth_token.key
	except:
		pass
		
	if not token:
		Token.objects.create(user=instance)