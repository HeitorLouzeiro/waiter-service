# Generated by Django 4.1 on 2023-05-11 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('customers', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('type', models.CharField(choices=[('prim_attendance', 'First Call'), ('service', 'Service'), ('closed', 'Closed'), ('deliver', 'Deliver')], max_length=16)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('done', 'Done')], default='pending', max_length=9)),
                ('hr_creation', models.DateTimeField(auto_now_add=True)),
                ('hr_service', models.DateTimeField(blank=True, null=True)),
                ('table', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='customers.table')),
                ('waiter', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Delivery',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='customers.itemorder')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='waiter.task')),
            ],
        ),
    ]
