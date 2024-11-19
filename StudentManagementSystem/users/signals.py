from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
import logging
from django.contrib.auth.models import User

logger = logging.getLogger('myapp')

@receiver(post_save, sender=User)
def log_user_registration(sender, instance, created, **kwargs):
    if created:
        logger.info(f'New user registered: {instance.username} (Email: {instance.email})')
        
@receiver(user_logged_in)
def log_user_login(sender, request, user, **kwargs):
    logger.info(f'User logged in: {user.username} (IP: {request.META["REMOTE_ADDR"]})')

@receiver(user_logged_out)
def log_user_logout(sender, request, user, **kwargs):
    logger.info(f'User logged out: {user.username} (IP: {request.META["REMOTE_ADDR"]})')
