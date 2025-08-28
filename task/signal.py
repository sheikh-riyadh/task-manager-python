from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
from task.models import Task, Employee

# We will notify when after task is completed this is called "post_save signal"
@receiver(post_save, sender=Task)
def notify_created_task(sender, instance, created, **kwargs):
    if created:
        instance.is_completed = True
        instance.save()
        print("Completed")


@receiver(pre_save, sender=Employee)
def notify_employee(sender, instance, **kwargs):
    print('Get notified employee')


@receiver(m2m_changed, sender=Task.assigned_to.through)
def send_email_notification_employee(sender, instance, action, **kwargs):

    emails_list = [employee.email for employee in instance.assigned_to.all()]

    if action == 'post_add':
        send_mail(
    "New task assigned",
    f"You have assinged new task : {instance.project.name}",
    "sheikhriyad350883@gmail.com",
    emails_list,
    )