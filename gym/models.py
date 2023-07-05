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
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE ,blank=True, null=True)
    trainee = models.ManyToManyField(Trainee, blank=True, null=True)
    gym = models.ForeignKey('Gym' , on_delete=models.CASCADE, blank=True, null=True)


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
    description = models.TextField()
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name='gym')
    contacts = models.TextField()
    phone_number = models.OneToOneField(PhoneNumber, on_delete=models.CASCADE)
    location = models.ForeignKey(MapLocation, on_delete=models.SET_NULL, null=True, blank=True)


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


class Invitation(models.Model):
    gym = models.ForeignKey(Gym, on_delete=models.CASCADE)
    trainer = models.ForeignKey(Trainer, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['gym', 'trainer']

    def __str__(self):
        return f'gym: {self.gym.name} , trainer: {self.trainer.user.email} '
