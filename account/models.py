from django.db import models


class BaseUser(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.IntegerField(null=True)
    email = models.EmailField(max_length=250, unique=True, null=True)

    class Meta:
        abstract = True


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=11, unique=True)


class Trainee(BaseUser):
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    height = models.FloatField()
    weight = models.FloatField()
=======
class GymOwnerPhoneNumber(PhoneNumber):
    gym_owner = models.ForeignKey('GymOwner', on_delete=models.CASCADE, related_name='phone_number')


class GymOwner(BaseUser):
    license_number = models.CharField(max_length=64, unique=True)

