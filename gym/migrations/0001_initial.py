# Generated by Django 3.2 on 2023-05-22 08:46

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='City',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Province',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='SportField',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='Gym',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('logo_image', models.ImageField(upload_to='gym/logo/')),
                ('background_image', models.ImageField(upload_to='gym/background/')),
                ('description', models.TextField()),
                ('contacts', models.TextField()),
                ('city', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gym', to='gym.city')),
                ('gym_owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.gymowner')),
                ('phone_number', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='account.phonenumber')),
                ('sport_filed', models.ManyToManyField(to='gym.SportField')),
            ],
        ),
        migrations.AddField(
            model_name='city',
            name='province',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='city', to='gym.province'),
        ),
        migrations.CreateModel(
            name='TrainerPreRegistration',
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
        migrations.CreateModel(
            name='TraineePreRegistration',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.trainee')),
            ],
            options={
                'unique_together': {('gym', 'trainee')},
            },
        ),
        migrations.CreateModel(
            name='GymTrainer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
                ('trainer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.trainer')),
            ],
            options={
                'unique_together': {('gym', 'trainer')},
            },
        ),
        migrations.CreateModel(
            name='GymTrainee',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gym', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='gym.gym')),
                ('trainee', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.trainee')),
            ],
            options={
                'unique_together': {('gym', 'trainee')},
            },
        ),
    ]
