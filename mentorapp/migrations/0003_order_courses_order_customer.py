# Generated by Django 5.1.3 on 2024-11-21 14:57

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorapp', '0002_courses_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='courses',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentorapp.courses'),
        ),
        migrations.AddField(
            model_name='order',
            name='customer',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='mentorapp.customer'),
        ),
    ]