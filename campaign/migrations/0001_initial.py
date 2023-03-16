# Generated by Django 4.1.7 on 2023-03-09 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Campaign',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('status', models.CharField(choices=[('CREATED', 'CREATED'), ('UNDER REVIEW', 'UNDER REVIEW'), ('CHANGES REQUESTED', 'CHANGES REQUESTED'), ('APPROVED', 'APPROVED'), ('LIVE', 'LIVE'), ('COMPLETED', 'COMPLETED'), ('REFUNDED', 'REFUNDED'), ('CLOSED', 'CLOSED')], default='CREATED', max_length=100)),
                ('youtube_link', models.TextField(null=True)),
                ('ama_date', models.DateField(null=True)),
                ('ama_meet_link', models.TextField(null=True)),
                ('ama_youtube_video', models.TextField(null=True)),
                ('pitch', models.TextField(null=True)),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]
