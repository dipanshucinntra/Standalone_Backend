from django.contrib.auth import login, logout

from rest_framework import generics
from rest_framework import permissions
from rest_framework import status
from rest_framework import views
from rest_framework.response import Response

from django.http import HttpResponseRedirect

from . import serializers
#from .models import Employee
#from users.serializers import EmployeeSerializer
from django.contrib.sessions.models import Session

from rest_framework.decorators import api_view
from django.views import View

class LoginView(views.APIView):
    # This view should be accessible also for unauthenticated users.
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = serializers.LoginSerializer(data=self.request.data, context={ 'request': self.request })
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        #request.session.set_expiry(60) # for overwride setting cookies age
        #print(request.session.get_expiry_age())
        #print(request.session.session_key)
        return Response({"SessionId":request.session.session_key, "SessionTimeout": int(request.session.get_expiry_age()/60)}, status=status.HTTP_202_ACCEPTED)
        #return Response(None, status=status.HTTP_202_ACCEPTED)


class LogoutView(views.APIView):

    def get(self, request, format=None):
        logout(request)
        return HttpResponseRedirect(redirect_to='/login/') # done
        #return Response({"message":"Logout success"}, status=status.HTTP_204_NO_CONTENT) # done
        #return Response(status=status.HTTP_204_NO_CONTENT) # done


class ProfileView(generics.RetrieveAPIView):
    serializer_class = serializers.UserSerializer

    def get_object(self):
        return self.request.user

"""
#User All API
@api_view(["GET"])
def EmployeeViewOne(self, pk):
    try:
        user_obj = Employee.objects.get(pk=pk) 
        user_json = EmployeeSerializer(user_obj, many=False)
        return Response({"message": "success","status": 200,"data":user_json.data})
    except Exception as e:
        return Response({"message": str(e),"status": 201,"data":[]})


#working
class EmployeeView(generics.RetrieveAPIView):
    def get(self, request, pk=None):
        user_obj = Employee.objects.get(pk=pk)
        user_json = EmployeeSerializer(user_obj, many=False)
        return Response({"message": "success","status": 200,"data":user_json.data})

class EmployeeCreate(generics.CreateAPIView):
    serializer_class = serializers.EmployeeSerializer
    def post(self, request):
        try:
            model = Employee(username=request.data['username'], password=request.data['password'], email=request.data['email'], fname=request.data['fname'], lname=request.data['lname'])
            model.full_clean()
            model.save()
            em = Employee.objects.latest('id')
            return Response({"message": "success","status": 200,"data":[{"id":em.id}]})
        except Exception as e:    
            return Response({"message": str(e),"status": 201,"data":[]})
"""            
            