from django.db import models
from django.contrib.auth.models import User
from django.core.validators import RegexValidator

class Profile(models.Model):
    ROLE_CHOICES = [("patient", "Patient"), ("doctor", "Doctor")]
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default="patient")
    phone = models.CharField(max_length=15, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    qualification = models.CharField(max_length=150, blank=True)
    experience_years = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.user.username} ({self.role})"

class Appointment(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"), ("approved", "Approved"),
        ("rejected", "Rejected"), ("cancelled", "Cancelled"),
        ("completed", "Completed"),
    ]
    patient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="patient_appointments")
    doctor = models.ForeignKey(User, on_delete=models.CASCADE, related_name="doctor_appointments")
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    reason = models.TextField()
    status = models.CharField(max_length=12, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-appointment_date", "-appointment_time"]
        constraints = [
            models.UniqueConstraint(
                fields=["doctor", "appointment_date", "appointment_time"],
                condition=models.Q(status__in=["pending", "approved"]),
                name="unique_active_doctor_slot",
            )
        ]

    def __str__(self):
        return f"{self.patient.username} → {self.doctor.username} ({self.appointment_date})"
