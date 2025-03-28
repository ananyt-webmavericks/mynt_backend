# Generated by Django 4.1.7 on 2023-03-09 08:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('campaign', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rewards',
            fields=[
                ('id', models.BigAutoField(primary_key=True, serialize=False)),
                ('amount', models.CharField(max_length=12)),
                ('product_name', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('created_at', models.DateTimeField()),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('campaign_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='campaign.campaign')),
            ],
        ),
    ]
