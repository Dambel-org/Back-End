# Generated by Django 3.2 on 2023-07-06 19:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_baseuser_verify_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='verified',
            field=models.BooleanField(default=False),
        ),
    ]
