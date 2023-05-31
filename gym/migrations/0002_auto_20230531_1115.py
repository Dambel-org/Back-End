# Generated by Django 3.2 on 2023-05-31 11:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('gym', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='MapLocation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('longitude', models.DecimalField(decimal_places=6, max_digits=9)),
                ('address', models.CharField(max_length=255)),
            ],
        ),
        migrations.AddField(
            model_name='gym',
            name='location',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='gym.maplocation'),
        ),
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.trainer')),
            ],
            options={
                'unique_together': {('gym', 'trainer')},
            },
        ),
    ]
