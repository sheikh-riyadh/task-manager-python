# Generated by Django 5.1.7 on 2025-03-21 05:54

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('start_date', models.DateField()),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=250)),
                ('description', models.TextField()),
                ('due_date', models.DateField()),
                ('status', models.CharField(choices=[('PENDING', 'Pending'), ('IN_PROGRESS', 'In Progress'), ('COMPLETED', 'Completed')], default='PENDING', max_length=15)),
                ('is_completed', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('assigned_to', models.ManyToManyField(related_name='task', to='task.employee')),
                ('project', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='task', to='task.project')),
            ],
        ),
        migrations.CreateModel(
            name='TaskDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('assigned_to', models.CharField(max_length=100)),
                ('priority', models.CharField(choices=[('H', 'HIGH'), ('M', 'MEDIUM'), ('L', 'LOW')], default='L', max_length=1)),
                ('notes', models.TextField(blank=True, null=True)),
                ('task', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='details', to='task.task')),
            ],
        ),
    ]
