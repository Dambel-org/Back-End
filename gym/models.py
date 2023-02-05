from django.db import models

from account.models import GymOwner, Trainee, Trainer


class Gym(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    gym_owner = models.ForeignKey(GymOwner, on_delete=models.CASCADE)


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
