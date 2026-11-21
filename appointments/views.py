from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from .forms import RegisterForm, AppointmentForm
from .models import Profile, Appointment

def home(request):
    doctors = User.objects.filter(profile__role="doctor", profile__is_available=True).select_related("profile")
    return render(request, "appointments/home.html", {"doctors": doctors[:6]})

def register_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account has been created.")
        return redirect("dashboard")
    return render(request, "appointments/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("dashboard")
    return render(request, "appointments/login.html", {"form": form})

@login_required
@require_POST
def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("home")

@login_required
def dashboard(request):
    profile = request.user.profile
    if profile.role == "doctor":
        appointments = Appointment.objects.filter(doctor=request.user).select_related("patient")
        return render(request, "appointments/doctor_dashboard.html", {"appointments": appointments})
    appointments = Appointment.objects.filter(patient=request.user).select_related("doctor", "doctor__profile")
    return render(request, "appointments/patient_dashboard.html", {"appointments": appointments})

def doctor_list(request):
    doctors = User.objects.filter(profile__role="doctor", profile__is_available=True).select_related("profile")
    specialization = request.GET.get("specialization", "").strip()
    if specialization:
        doctors = doctors.filter(profile__specialization__icontains=specialization)
    return render(request, "appointments/doctors.html", {"doctors": doctors, "specialization": specialization})

@login_required
def book_appointment(request, doctor_id):
    if request.user.profile.role != "patient":
        messages.error(request, "Only patient accounts can book appointments.")
        return redirect("dashboard")
    doctor = get_object_or_404(User, pk=doctor_id, profile__role="doctor", profile__is_available=True)
    form = AppointmentForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        appointment = form.save(commit=False)
        appointment.patient = request.user
        appointment.doctor = doctor
        try:
            appointment.save()
            messages.success(request, "Appointment request submitted. Wait for the doctor's response.")
            return redirect("dashboard")
        except IntegrityError:
            form.add_error(None, "That time slot is already requested or booked. Please choose another time.")
    return render(request, "appointments/book.html", {"form": form, "doctor": doctor})

@login_required
@require_POST
def update_appointment_status(request, appointment_id, status):
    if request.user.profile.role != "doctor" or status not in ["approved", "rejected", "completed"]:
        messages.error(request, "You are not allowed to perform that action.")
        return redirect("dashboard")
    appointment = get_object_or_404(Appointment, pk=appointment_id, doctor=request.user)
    if appointment.status in ["cancelled", "rejected", "completed"]:
        messages.error(request, "This appointment can no longer be changed.")
    else:
        appointment.status = status
        appointment.save()
        messages.success(request, f"Appointment marked as {status}.")
    return redirect("dashboard")

@login_required
@require_POST
def cancel_appointment(request, appointment_id):
    appointment = get_object_or_404(Appointment, pk=appointment_id, patient=request.user)
    if appointment.status in ["pending", "approved"]:
        appointment.status = "cancelled"
        appointment.save()
        messages.success(request, "Appointment cancelled.")
    else:
        messages.error(request, "This appointment cannot be cancelled.")
    return redirect("dashboard")

def doctor_detail(request, doctor_id):
    doctor = get_object_or_404(User, pk=doctor_id, profile__role="doctor")
    return render(request, "appointments/doctor_detail.html", {"doctor": doctor})
