# Generated by Django 3.2 on 2023-07-06 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='baseuser',
            name='reset_code',
            field=models.IntegerField(blank=True, max_length=6, null=True),
        ),
    ]
