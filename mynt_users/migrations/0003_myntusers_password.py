# Generated by Django 4.1.7 on 2023-04-03 07:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mynt_users', '0002_alter_myntusers_user_type'),
    ]

    operations = [
        migrations.AddField(
            model_name='myntusers',
            name='password',
            field=models.CharField(max_length=12, null=True),
        ),
    ]
