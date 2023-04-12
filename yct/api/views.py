from django.shortcuts import render
from helpers.views import BaseView
from .models import SchoolUser, Course, Department
from rest_framework.response import Response
from rest_framework import status
from .helper import jsonify_user
from rest_framework_simplejwt.tokens import RefreshToken
from .helper import jsonify_user
from rest_framework.decorators import api_view, APIView


# Create your views here.
class SignUpStudent(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "matric_no", "date_of_birth", "home_address", "programme", "school", "department", "level", "place_of_birth", "state_of_origin", "local_government_area", "parent_name", "parent_address", "parent_contact","password"]
    def post(self, request, format=None):
        # Call Query Field
        email=request.data.get("email")
        matric_no = request.data.get("matric_no")
        password = request.data.get("password")
        
        #CHECK IF EMAIL EXISTS
        if SchoolUser.objects.filter(email=email).exists():
            res={
                "code": 400,
                "message":"Email is taken"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
       
        # CHECK IF STUDENT MATRIC NUMBER EXISTS
        if SchoolUser.objects.filter(matric_no=matric_no).exists():
            res={
                "code": 400,
                "message": "Matric Number Exists"
            }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        # Check If User Sends Password
        if not password:
            res = {
                "code":400,
                "message": "Password is Required"
                }
            return Response(res, status=status.HTTP_400_BAD_REQUEST)
        
        student = SchoolUser()
        student.first_name = request.data.get("first_name")
        student.last_name = request.data.get("last_name")
        student.date_of_birth = request.data.get("date_of_birth")
        student.home_address = request.data.get("home_address")
        student.programme = request.data.get("programme")
        student.school = request.data.get("school")
        student.department = request.data.get("department")
        student.level = request.data.get("level")
        student.place_of_birth = request.data.get("place_of_birth")
        student.state_of_origin = request.data.get("state_of_origin")
        student.local_government_area = request.data.get("local_government_area")
        student.parent_name = request.data.get("parent_name")
        student.parent_address = request.data.get("parent_address")
        student.parent_contact = request.data.get("parent_contact")
        student.matric_no = matric_no
        student.email = email
        student.set_password(raw_password=request.data.get("password"))
        student.is_student=True
        student.save()
        res = {
            "status": self.is_success(),
            "data": jsonify_user(student)
            }
        return Response(res, status=status.HTTP_201_CREATED)

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