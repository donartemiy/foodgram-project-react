# Generated by Django 3.2 on 2023-08-02 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_subscription_non selfsubcribtion'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'default_related_name': 'user', 'ordering': ['username'], 'verbose_name': 'Пользователь', 'verbose_name_plural': 'Пользователи'},
        ),
    ]
