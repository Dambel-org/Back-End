from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from account.models import GymOwner, Trainee, Trainer, PhoneNumber


class Province(models.Model):
    name = models.CharField(max_length=50)


class City(models.Model):
    name = models.CharField(max_length=50)
    province = models.ForeignKey(Province, on_delete=models.CASCADE, related_name='city')


class Plan(models.Model):
    name = models.CharField(max_length=200)
    time_start = models.TimeField(default="0")
    time_end = models.TimeField(default="0")
    price = models.CharField(max_length=10, default=0, blank=True, null=True)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE, blank=True, null=True)
    trainee = models.ManyToManyField(Trainee, blank=True, null=True)
    gym = models.ForeignKey('Gym', on_delete=models.CASCADE, blank=True, null=True, related_name='plans')


class MapLocation(models.Model):
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    address = models.CharField(max_length=255)

    def __str__(self):
        return f"Latitude: {self.latitude}, Longitude: {self.longitude}"


class Gym(models.Model):
    gym_owner = models.ForeignKey(GymOwner, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    logo_image = models.ImageField(upload_to='gym/logo/')
    background_image = models.ImageField(upload_to='gym/background/')
    license_image = models.ImageField(upload_to='gym/license/', default=None, null=True, blank=True)
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='gym')
    contacts = models.TextField()
    location = models.ForeignKey(MapLocation, on_delete=models.SET_NULL, null=True, blank=True)


class Comment(models.Model):
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    rate = models.IntegerField(default=1, validators=[MaxValueValidator(5), MinValueValidator(1)])
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)


class TrainerPreRegistration(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['gym', 'trainer']


class TraineePreRegistration(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['gym', 'trainee']


class GymTrainee(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['gym', 'trainee']


class GymTrainer(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['gym', 'trainer']


class TrainerInvitation(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['gym', 'trainer']

    def __str__(self):
        return f'gym: {self.gym.name} , trainer: {self.trainer.user.email} '


class TraineeRequest(models.Model):
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    trainee = models.ForeignKey(Trainee, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['plan', 'trainee']

    def __str__(self):
        return f'gym: {self.plan.name} , trainer: {self.trainee.user.email}'
