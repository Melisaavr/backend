from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.exceptions import ValidationError


class User(AbstractUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'full_name']


class Slot(models.Model):
    DAY_CHOICES = [
        ('MON', 'Monday'),
        ('TUE', 'Tuesday'),
        ('WED', 'Wednesday'),
        ('THU', 'Thursday'),
        ('FRI', 'Friday'),
        ('SAT', 'Saturday'),
        ('SUN', 'Sunday'),
    ]

    day = models.CharField(max_length=3, choices=DAY_CHOICES)
    start_time = models.TimeField()
    end_time = models.TimeField()
    seats = models.IntegerField(default=5, validators=[
                                MinValueValidator(1), MaxValueValidator(10)])


class Booking(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    slot = models.ForeignKey(Slot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'slot')

    def clean(self):
        if self.slot.seats <= 0:
            raise ValidationError("No seats available for this slot.")
        if Booking.objects.filter(user=self.user, slot__day=self.slot.day, slot__start_time=self.slot.start_time).exists():
            raise ValidationError(
                "You have already booked a slot for this time.")

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
        self.slot.seats -= 1
        self.slot.save()

    def delete(self, *args, **kwargs):
        self.slot.seats += 1
        self.slot.save()
        super().delete(*args, **kwargs)
