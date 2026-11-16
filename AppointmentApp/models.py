
from django.db import models
from AccountApp.models import Doctor,Patient

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

    class Meta:
        ordering = ["appointment_date"]

        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date"],
                name="unique_patient-doctor-date",
                violation_error_message="ce docteur possède un rdv avec cette date"
            )
        ]
