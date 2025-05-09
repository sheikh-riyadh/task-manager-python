from django.db import models
from django.db.models.signals import post_save, pre_save, m2m_changed
from django.dispatch import receiver
from django.core.mail import send_mail
# Create your models here.


class Employee(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name



class Task(models.Model):
    STATUS_OPTIONS=(
        ("PENDING", "Pending"),
        ("IN_PROGRESS", "In Progress"),
        ("COMPLETED", "Completed")
    )
    project = models.ForeignKey("Project", on_delete=models.CASCADE, default=1, related_name="task")
    assigned_to = models.ManyToManyField(Employee, related_name="task")
    title = models.CharField(max_length=250)
    description = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length=15, choices=STATUS_OPTIONS, default="PENDING")
    is_completed = models.BooleanField(default=False)
    created_at= models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title



class TaskDetail(models.Model):
    HIGH='H'
    MEDIUM='M'
    LOW='L'

    PRIORITY_OPTIONS = (
        (HIGH,'HIGH'),
        (MEDIUM,'MEDIUM'),
        (LOW, 'LOW')
    )

    task = models.OneToOneField(Task,on_delete=models.CASCADE, related_name="details")
    # assigned_to = models.CharField(max_length=100)
    priority = models.CharField(max_length=1, choices=PRIORITY_OPTIONS, default=LOW)
    notes = models.TextField(blank=True, null=True)


    def __str__(self):
        return f"Details form task {self.task.title}"





class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    start_date = models.DateField()

    def __str__(self):
        return self.name


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
    
