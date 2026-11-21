from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Appointment
from datetime import date

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=False)
    role = forms.ChoiceField(choices=Profile.ROLE_CHOICES)
    phone = forms.CharField(max_length=15, required=False)
    specialization = forms.CharField(max_length=100, required=False)
    qualification = forms.CharField(max_length=150, required=False)
    experience_years = forms.IntegerField(min_value=0, required=False, initial=0)
    bio = forms.CharField(widget=forms.Textarea(attrs={"rows": 3}), required=False)
    consultation_fee = forms.DecimalField(max_digits=8, decimal_places=2, min_value=0, required=False, initial=0)

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email", "role", "phone",
                  "specialization", "qualification", "experience_years", "bio",
                  "consultation_fee", "password1", "password2")

    def clean(self):
        cleaned = super().clean()
        if cleaned.get("role") == "doctor" and not cleaned.get("specialization"):
            self.add_error("specialization", "Please enter your medical specialization.")
        return cleaned

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name = self.cleaned_data["first_name"]
        user.last_name = self.cleaned_data["last_name"]
        if commit:
            user.save()
            Profile.objects.create(
                user=user, role=self.cleaned_data["role"], phone=self.cleaned_data.get("phone", ""),
                specialization=self.cleaned_data.get("specialization", ""),
                qualification=self.cleaned_data.get("qualification", ""),
                experience_years=self.cleaned_data.get("experience_years") or 0,
                bio=self.cleaned_data.get("bio", ""),
                consultation_fee=self.cleaned_data.get("consultation_fee") or 0,
            )
        return user

class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        fields = ["appointment_date", "appointment_time", "reason"]
        widgets = {
            "appointment_date": forms.DateInput(attrs={"type": "date", "min": date.today().isoformat()}),
            "appointment_time": forms.TimeInput(attrs={"type": "time"}),
            "reason": forms.Textarea(attrs={"rows": 4, "placeholder": "Briefly describe why you need an appointment"}),
        }

    def clean_appointment_date(self):
        value = self.cleaned_data["appointment_date"]
        if value < date.today():
            raise forms.ValidationError("Appointment date cannot be in the past.")
        return value
