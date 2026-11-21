from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("register/", views.register_view, name="register"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("doctors/", views.doctor_list, name="doctors"),
    path("doctors/<int:doctor_id>/", views.doctor_detail, name="doctor_detail"),
    path("doctors/<int:doctor_id>/book/", views.book_appointment, name="book_appointment"),
    path("appointments/<int:appointment_id>/<str:status>/", views.update_appointment_status, name="update_status"),
    path("appointments/<int:appointment_id>/cancel/", views.cancel_appointment, name="cancel_appointment"),
]
