# Generated by Django 4.1.7 on 2023-09-21 13:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('interest', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='interest',
            name='amount',
            field=models.CharField(default=0, max_length=10),
        ),
    ]
