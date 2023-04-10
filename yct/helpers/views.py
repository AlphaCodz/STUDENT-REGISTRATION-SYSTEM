from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from api.models import SchoolUser
from api.helper import jsonify_user

class BaseView(APIView):
    """
    Alternative to Serializers
    input list of required fields into required_post_fields
    e.g
    class <ClassName>(BaseView):
        required_post_fields=["field1", "field2", "field3"]
    """
    required_post_fields=set()
    
    """List of Needed fields from the models
    """
    def post(self, request, format=None):
            for field in self.required_post_fields:
                if not request.data.get(field):
                    res = {
                        "code": 404,
                        "message": f"{field} not found"
                    }
                    return Response(res, status=status.HTTP_404_NOT_FOUND)
                
    def is_success(self):
        return {
            "code":200,
            "message": "Success",
        }
        
    def field_exists(self, field):
        return {
            "code":400,
            "message": f"{field} already exists",
        }
    
   