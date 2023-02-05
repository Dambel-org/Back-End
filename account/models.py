from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class BaseUserManager(UserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_user(email, password, **extra_fields)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class BaseUser(AbstractUser):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.IntegerField(null=True)
    email = models.EmailField(max_length=250, unique=True, null=True)
    objects = BaseUserManager()
    username = None
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age']
    USERNAME_FIELD = 'email'


class PhoneNumber(models.Model):
    number = models.CharField(max_length=11, unique=True)


class Trainer(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='trainer')
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'


class Trainee(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()

    class Meta:
        verbose_name = 'Trainee'
        verbose_name_plural = 'Trainees'


class GymOwnerPhoneNumber(PhoneNumber):
    gym_owner = models.ForeignKey('GymOwner', on_delete=models.CASCADE, related_name='phone_number')


class GymOwner(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    license_number = models.CharField(max_length=64, unique=True)

    class Meta:
        verbose_name = 'Gym Owner'
        verbose_name_plural = 'Gym Owners'
