from django.shortcuts import render
from helpers.views import BaseView
from .models import SchoolUser, Course, Department, Programme, Session, Level
from rest_framework.response import Response
from rest_framework import status, generics
from .helper import jsonify_user
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import jsonify_user
from rest_framework.decorators import api_view, APIView
from .serializers import SchoolUserSerializer, CourseSerializer
from django.db import transaction
from .paystack import PaymentProcessor
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse

class SignUpStudent(APIView):
    serializer_class = SchoolUserSerializer
    def post(self, request, format=None):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpBursar(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "staff_id"]
    def post(self, request, format=None):
        data = request.data
        
            # Call Query Field
        email=data.get("email")
        staff_id=data.get("staff_id")
        password=data.get("password")
        
        #CHECK IF EMAIL EXISTS
        if SchoolUser.objects.filter(email=email).exists():
            res={
                "code": 400,
                "message":"Email is taken"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
       
        # CHECK IF STUDENT MATRIC NUMBER EXISTS
        if SchoolUser.objects.filter(staff_id=staff_id).exists():
            res={
                "code": 400,
                "message": "Staff id Exists"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        # Check If User Sends Password
        if not password:
            res = {
                "code":400,
                "message": "Password is Required"
                }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        bursar = SchoolUser()
        bursar.first_name = data["first_name"]
        bursar.last_name = data["last_name"]
        bursar.staff_id = staff_id
        bursar.email = email
        bursar.set_password(raw_password=data.get("password"))
        bursar.is_bursar=True
        bursar.save()
        res = {
            "status": self.is_success(),
            "data": jsonify_user(bursar)
            }
        return Response(res, status=status.HTTP_201_CREATED)
        
        
class LoginStudent(BaseView):
    required_post_fields = ["matric_no", "password"]
    def post(self, request):
        student = SchoolUser.objects.filter(matric_no=request.data.get("matric_no")).first()
        if not student:
            res = {
                "code":404,
                "message": "Student doesn't exist"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        if student.check_password(raw_password=request.data.get("password")):
            token = RefreshToken.for_user(student)
            print(token)
            res = {
                "code":200,
                "message": "Login Successful",
                "student_data": jsonify_user(student),
                "token": str(token.access_token)
            }
            return Response(res, status=status.HTTP_200_OK)
        res = {
            "code":401,
            "message": "Incorrect Password"
        }
        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    
class LoginStaff(BaseView):
    required_post_fields = ["staff_id", "password"]
    def post(self, request):
        staff = SchoolUser.objects.filter(staff_id=request.data.get("staff_id")).first()
        if not staff:
            res = {
                "code":404,
                "message": "Staff doesn't exist"
            }
            return Response(res, status=status.HTTP_404_NOT_FOUND)
        if staff.check_password(raw_password=request.data.get("password")):
            token = RefreshToken.for_user(staff)
            print(token)
            res = {
                "code":200,
                "message": "Login Successful",
                "staff_data": jsonify_user(staff),
                "token": str(token.access_token)
            }
            return Response(res, status=status.HTTP_200_OK)
        res = {
            "code":401,
            "message": "Incorrect Password"
        }
        return Response(res, status=status.HTTP_401_UNAUTHORIZED)
    
    
# FUNCTIONALITIES
class CreateDepartment(APIView):
    def post(self, request, format=None):
        department = Department.objects.filter(department=request.data["department"]).exists()
        if department:
            res = {
                "code": 400,
                "message": "Department Already Exists"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        department = Department.objects.create(
            department=request.data["department"]
        )
        res = {
            "code": 201,
            "message": f"Department {department} added successfully"
        }
        return Response(res, status=status.HTTP_201_CREATED)
    
class CreateCourseView(generics.CreateAPIView):
    serializer_class = CourseSerializer

@api_view(["POST"])
def create_courses(request, id):
    data=request.data
    if not isinstance(data, list):
        return Response({"error": "Invalid data format. You cannot register only one course"})
    
    # department id
    try:
        dep_id=Department.objects.get(id=id)
    except Department.DoesNotExist:
        return Response({"error": f"id {dep_id} does not exist"})
    
    courses = []
    for course_data in data:
        # check is a course whith the same title and code already exists
        existing_course = Course.objects.filter(department=dep_id, title=course_data["title"], code=course_data["code"]).first()
        if existing_course:
            courses.append(existing_course)
        else:
            course = Course(department=dep_id, title=course_data['title'], code=course_data["code"])
            course.save()
            courses.append(course)        
    return Response({'courses': [(course.id, course.title, course.code) for course in courses]})

# CREATE 


class CreateCourseProgrammeDepartmentLevelView(APIView):
    @transaction.atomic
    def post(self, request, format=None):
        course_data = request.data.get('course_data', {})
        programme_data = request.data.get('programme_data', {})
        department_data = request.data.get('department_data', {})
        level_data = request.data.get('level_data', {})
        
        # Create Department
        department = Department.objects.create(**department_data)
        department_id = department.id
        # Create Programme
        programme = Programme.objects.create(**programme_data)
        programme_id = programme.id

        # Create Level
        level = Level.objects.create(**level_data)
        level_id = level.id

        # Create Course
        course_data['department'] = department
        course_data['level'] = level
        course = Course.objects.create(**course_data)
        course_id = course.id

        return Response({'course_id': course_id, 'programme_id': programme_id, 'department_id': department_id, 'level_id': level_id}, status=status.HTTP_201_CREATED)

@csrf_exempt
def initializer_payment(request):
    if request.method == "POST":
        email= request.POST.get('email')
        amount= request.POST.get('amount')
        processor = PaymentProcessor(secret_key='sk_test_8bf0c5575575a946142b892294b33cc28dbf57f9')
        url=processor.initialize_payment(email, amount)
        return JsonResponse({'url':url})