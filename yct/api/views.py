from django.shortcuts import render
from helpers.views import BaseView
from .models import SchoolUser
from rest_framework.response import Response
from rest_framework import status
from .helper import jsonify_user

# Create your views here.
class SignUpStudent(BaseView):
    required_post_fields = ["first_name", "last_name", "email", "matric_no", "password"]
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
            # Call Query Field
        email=request.data.get("email")
        staff_id = request.data.get("staff_id")
        password = request.data.get("password")
        
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
        bursar.first_name = request.data.get("first_name")
        bursar.last_name = request.data.get("last_name")
        bursar.staff_id = staff_id
        bursar.email = email
        bursar.set_password(raw_password=request.data.get("password"))
        bursar.is_bursar=True
        bursar.save()
        res = {
            "status": self.is_success(),
            "data": jsonify_user(bursar)
            }
        return Response(res, status=status.HTTP_201_CREATED)
        
