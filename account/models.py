from django.db import models


class BaseUser(models.Model):
    first_name = models.CharField(max_length=250)
    last_name = models.CharField(max_length=250)
    age = models.IntegerField(null=True)
    email = models.EmailField(max_length=250, unique=True, null=True)
    phone = models.OneToOneRel

    class Meta:
        abstract = True


class PhoneNumber(models.Model):
    phone_number = models.CharField(max_length=11)

    class Meta:
        abstract = True


class GymOwnerPhoneNumber(models.Model):
    phone = models.OneToOneRel(PhoneNumber, on_delete=models.CASCADE, related_name='gym_owner_phone_number')
    gym_owner = models.ForeignKey('GymOwner', on_delete=models.CASCADE, related_name='gym_owner')


class GymOwner(models.Model):
    user = models.OneToOneRel(BaseUser, on_delete=models.CASCADE, related_name='gym_owner')
    license_number = models.CharField(max_length=64, unique=True)
