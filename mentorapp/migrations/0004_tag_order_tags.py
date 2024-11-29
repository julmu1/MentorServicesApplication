# Generated by Django 5.1.3 on 2024-11-21 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mentorapp', '0003_order_courses_order_customer'),
    ]

    operations = [
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, null=True)),
            ],
        ),
        migrations.AddField(
            model_name='order',
            name='tags',
            field=models.ManyToManyField(to='mentorapp.tag'),
        ),
    ]
