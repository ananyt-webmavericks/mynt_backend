# Generated by Django 4.1.7 on 2023-03-30 03:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rewards', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='rewards',
            name='description',
        ),
        migrations.AddField(
            model_name='rewards',
            name='discounted_price',
            field=models.IntegerField(null=True),
        ),
    ]
