# Generated by Django 5.1.3 on 2024-11-21 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorapp', '0004_tag_order_tags'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='tags',
        ),
        migrations.AddField(
            model_name='courses',
            name='tags',
            field=models.ManyToManyField(to='mentorapp.tag'),
        ),
    ]
