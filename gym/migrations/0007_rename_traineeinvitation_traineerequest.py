# Generated by Django 3.2 on 2023-07-09 21:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0005_auto_20230709_2232'),
        ('gym', '0006_traineeinvitation'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='TraineeInvitation',
            new_name='TraineeRequest',
        ),
    ]
