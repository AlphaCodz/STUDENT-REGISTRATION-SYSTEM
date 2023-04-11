from .models import SchoolUser

def jsonify_user(user:SchoolUser):
    user_data={
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "email":user.email,
        "matric_no": user.matric_no,
        "staff_id": user.staff_id,
        "is_student": user.is_student,
        "is_bursar": user.is_bursar,
        "is_course_adviser": user.is_course_adviser,
        "biodata": []
        }
    if user.is_student==True:
            data={
                "programme": user.programme,
                "date_of_birth": user.date_of_birth,
                "home_address": user.home_address,
                "school": user.school,
                "department": user.department,
                "level": user.level,
                "place_of_birth": user.place_of_birth,
                "state_of_origin": user.state_of_origin,
                "local_government_area": user.local_government_area,
                "parent_name": user.parent_name,
                "parent_contact": user.parent_contact,
                "parent_address": user.parent_address
            }
            user_data["biodata"].append(data)
    return user_data
            
            
    
    
    