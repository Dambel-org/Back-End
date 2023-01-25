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
