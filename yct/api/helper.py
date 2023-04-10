from .models import SchoolUser

def jsonify_user(user:SchoolUser):
    return {
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email":user.email,
        "matric_no": user.matric_no,
        "staff_id": user.staff_id,
        "is_student": user.is_student,
        "is_bursar": user.is_bursar,
        "is_course_adviser": user.is_course_adviser
    }