# Generated by Django 4.1.7 on 2023-03-17 07:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='DealType',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('deal_name', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
