# serializers.py
from rest_framework import serializers
from .models import SchoolUser, Course


class SchoolUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = SchoolUser
        fields = (
            'id',
            'first_name',
            'last_name',
            'email',
            'matric_no',
            'staff_id',
            'date_of_birth',
            'home_address',
            'programme',
            'school',
            'department',
            'level',
            'session',
            'place_of_birth',
            'state_of_origin',
            'local_government_area',
            'parent_name',
            'parent_address',
            'parent_contact',
            'is_bursar',
            'is_student',
            'is_course_adviser',
            'password'
        )

    def create(self, validated_data):
        password = validated_data.pop('password')
        instance = SchoolUser(**validated_data)
        instance.set_password(password)
        instance.save()
        return instance
    
class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = "__all__"
        
    def create(self, validated_data):
        course = Course.objects.create(
            department = validated_data["department"],
            title = validated_data["title"],
            code = validated_data["code"],
            level = validated_data["level"]
        )
        course.save()
        return course