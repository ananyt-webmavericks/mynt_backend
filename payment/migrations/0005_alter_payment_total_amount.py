# Generated by Django 4.1.7 on 2024-08-27 11:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payment", "0004_payment_transaction_id"),
    ]

    operations = [
        migrations.AlterField(
            model_name="payment",
            name="total_amount",
            field=models.CharField(max_length=15, null=True),
        ),
    ]
