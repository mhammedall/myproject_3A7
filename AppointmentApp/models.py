
from django.db import models
from AccountApp.models import Doctor,Patient
from django.utils import timezone 
from django.core.exceptions import ValidationError


# Create your models here.


class Appointment(models.Model):
    reason = models.TextField()

    prescription = models.FileField(
        blank=True,
        upload_to='prescriptions/'
    )

    class Status(models.TextChoices):
        PENDING = "PENDING", "En attente"
        CONFIRMED = "CONFIRMED", "Confirmé"
        CANCELLED = "CANCELLED", "Annulé"

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.PENDING
    )

    # status = models.CharField(
    #     max_length=10,
    #     choices=[
    #         ("PENDING", "En attente"),
    #         ("CONFIRMED", "Confirmé")
    #     ],
    #     default="PENDING"
    # )

    duration_minutes = models.PositiveIntegerField(default=30)

    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    appointment_date = models.DateField()

    doctor = models.ForeignKey(
        Doctor,
        on_delete=models.CASCADE,
        related_name="appointments"
    )

    # patient = models.ForeignKey(
    #     "AccountApp.Patient",
    #     on_delete=models.CASCADE,
    #     related_name="appointments"
    # )

    patient = models.ForeignKey(
        Patient,
        on_delete=models.CASCADE,
        related_name="appointments"
    )
    def clean(self):
        modified_date=self._state.adding or (
            Appointment.objects.filter(
                pk=self.pk,appointment_date=self.appointment_date
            ).exists()

        )
        if modified_date and (self.appointment_date <= timezone.localdate()) :
            raise ValidationError("la date du rendez vous etre postéieur a la carte")


    class Meta:
        ordering = ["appointment_date"]

        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_patient-doctor-date",
                violation_error_message="ce docteur possède un rdv avec cette date"
            )
        ]
    def __str__(self):
        return f"le rdv est pour la raison {self.reason}"