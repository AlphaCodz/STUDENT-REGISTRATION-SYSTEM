from django.urls import path
from .views import SignUpStudent, SignUpBursar

urlpatterns = [
    path("reg/student", SignUpStudent.as_view(), name="SignupSTudent"),
    path("reg/bursar", SignUpBursar.as_view(), name="SignUpBursar")
]
