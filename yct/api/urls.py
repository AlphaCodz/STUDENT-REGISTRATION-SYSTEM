from django.urls import path
from .views import SignUpStudent, SignUpBursar, LoginStudent, LoginStaff, CreateDepartment, CreateCourseView, CreateCourseProgrammeDepartmentLevelView
from . import views


urlpatterns = [
    path("reg/student", SignUpStudent.as_view(), name="SignupSTudent"),
    path("reg/bursar", SignUpBursar.as_view(), name="SignUpBursar"),
    path("login/student", LoginStudent.as_view(), name="login-student"),
    path("login/staff", LoginStaff.as_view(), name="login-staff"),
    path("add/department", CreateDepartment.as_view(), name="create-department"),
    path("add/courses/<int:id>", views.create_courses, name="courses"),
    path("create/course", CreateCourseView.as_view(), name="create-course"),
    path("create/", CreateCourseProgrammeDepartmentLevelView.as_view(), name="create"),
    path('initialize-payment/', views.initializer_payment, name='initialize')
]
