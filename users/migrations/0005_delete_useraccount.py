# Generated by Django 5.1 on 2024-08-24 10:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_delete_user_useraccount_groups_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='UserAccount',
        ),
    ]
