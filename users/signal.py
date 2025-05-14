from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.tokens import default_token_generator
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth.models import User, Group


@receiver(post_save, sender=User)
def send_activation_email(sender, instance, created, **kwargs):
    if created:
        token = default_token_generator.make_token(instance)
        activation_url = f"{settings.URL}/user/activate/{instance.id}/{token}/"

        subject = 'Activate your account'
        message = f'Please {instance.username} active your account clicking the activation url below \n\n {activation_url} \n\n Thank you!'

        receipient_list = [instance.email]
        
        try:
            send_mail(subject,message,settings.EMAIL_HOST_USER,receipient_list)
        except Exception as e:
            print(f'Fail to send email {instance.username} with {str(e)} error')


@receiver(post_save, sender=User)
def asigned_role(sender, instance, created, **kwargs):
    if created:
        user_group = Group.objects.get_or_create(name="User")
        instance.groups.add(user_group)
        instance.save()