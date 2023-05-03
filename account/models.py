from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from gym.models import Province, City


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
    email = models.EmailField(max_length=250, unique=True, null=True)
    province = models.ForeignKey(Province, on_delete=models.SET_NULL)
    city = models.ForeignKey(City, on_delete=models.SET_NULL)

    username = None
    REQUIRED_FIELDS = ['first_name', 'last_name', 'age', 'password']
    USERNAME_FIELD = 'email'

    objects = BaseUserManager()

    def save(self, *args, **kwargs):
        if self.city:
            self.province = self.city.province
        super(BaseUser, self).save(*args, **kwargs)


class Trainer(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE, related_name='trainer')
    age = models.IntegerField(null=True)

    class Meta:
        verbose_name = 'Trainer'
        verbose_name_plural = 'Trainers'


class Trainee(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    age = models.IntegerField(null=True)
    height = models.FloatField()
    weight = models.FloatField()

    class Meta:
        verbose_name = 'Trainee'
        verbose_name_plural = 'Trainees'


class GymOwner(models.Model):
    user = models.OneToOneField(BaseUser, on_delete=models.CASCADE)
    # TODO validation for phone number
    phone_number = models.CharField(max_length=11)
    address = models.TextField()

    class Meta:
        verbose_name = 'Gym Owner'
        verbose_name_plural = 'Gym Owners'
