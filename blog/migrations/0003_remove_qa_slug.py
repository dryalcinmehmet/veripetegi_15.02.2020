# Generated by Django 2.2 on 2019-05-14 10:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_qa'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='qa',
            name='slug',
        ),
    ]
