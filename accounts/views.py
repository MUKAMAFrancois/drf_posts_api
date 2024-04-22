from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from .serializers import UserSerializer
from rest_framework.decorators import api_view
from rest_framework.request import Request
from .models import User
from drf_yasg.utils import swagger_auto_schema
import datetime
from .tokens import create_jwt_pair_for_user

# Create your views here.



class SignupView(APIView):
    @swagger_auto_schema(operation_description="Create a new user",request_body=UserSerializer,responses={201:UserSerializer})
    def post(self,request:Request):
        data=request.data
        serializer=UserSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            res={
               "msg":"User created successfully",
               "data":serializer.data
           }
            return Response(res,status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    


class LoginView(APIView):
    @swagger_auto_schema(operation_description="Login a user",request_body=UserSerializer,responses={200:UserSerializer})
    def post(self,request:Request):
        data=request.data
        email=data.get('email')
        password=data.get('password')
        if email is None or password is None:
            return Response({'error':'Please provide both email and password'},status=status.HTTP_400_BAD_REQUEST)
        user=authenticate(email=email,password=password)
        if not user:
            return Response({'error':'Invalid Credentials'},status=status.HTTP_401_UNAUTHORIZED)
        # token,created=Token.objects.get_or_create(user=user) #expires=datetime.datetime.now()+datetime.timedelta(hours=1))
        tokens=create_jwt_pair_for_user(user)
        res={
            "msg":"Login successful",
            "data":UserSerializer(instance=user).data,
            "tokens":tokens
        }
        return Response(data=res,status=status.HTTP_200_OK)
    



class LogoutView(APIView):
    permission_classes=[IsAuthenticated]
    @swagger_auto_schema(operation_description="Logout a user",responses={200:"Logged Out successfully"})
    def post(self,request:Request):
        try:
            token=Token.objects.get(user=request.user)
            token.delete()
            return Response({"msg":"Logged Out successfully"}, status=status.HTTP_200_OK)
        except Token.DoesNotExist:
            return Response({"error":"Invalid Token or user not logged in"},status=status.HTTP_400_BAD_REQUEST)
        

@api_view(http_method_names=["get"])
@swagger_auto_schema(operation_description="Get all users",responses={200:UserSerializer(many=True)})
def get_all_users(request:Request):
    users=User.objects.all()
    serializer=UserSerializer(instance=users,many=True)
    return Response(data=serializer.data,status=200)
        