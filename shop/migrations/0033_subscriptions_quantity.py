# Generated by Django 4.0.6 on 2022-12-30 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0032_positions_positions_userwise_subscriptions_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptions',
            name='quantity',
            field=models.IntegerField(default=0),
        ),
    ]