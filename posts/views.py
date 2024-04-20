import json
from django.shortcuts import render,get_object_or_404
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view,permission_classes
from rest_framework import status,generics,mixins,routers,relations,viewsets
from rest_framework.views import APIView
from .serializers import PostSerializer
from .models import Post
import uuid
from drf_yasg.utils import swagger_auto_schema


#function based API views



# @api_view(http_method_names=["get"])
# @swagger_auto_schema(operation_description="Get all posts",responses={200:PostSerializer(many=True)})
# def list_posts(request:Request):
#     posts=Post.objects.all()
#     serializer = PostSerializer(instance=posts,many=True)
#     return Response(data=serializer.data,status=200)




# @api_view(http_method_names=["POST"])
# @permission_classes([IsAuthenticated])
# @swagger_auto_schema(operation_description="Create a post",request_body=PostSerializer,responses={201:PostSerializer})
# def create_a_post(request:Request):
#     if request.method=="POST":
#         data=request.data
#         serializer=PostSerializer(data=data,context={"request":request}) #passing the request object to the serializer, 
#         #self.context['request'].user is used to get the current user making the request
#         if serializer.is_valid():
#             serializer.save()
#             res={
#                 "msg":"Post created successfully",
#                 "data":serializer.data
#             }
#             return Response(data=res,status=201)
#         return Response(data=serializer.errors,status=400)




# @api_view(http_method_names=["GET"])
# @swagger_auto_schema(operation_description="Get a single post",responses={200:PostSerializer})    
# def single_post(request,post_id:uuid.UUID):
#     post=get_object_or_404(Post,pk=post_id)
#     serializer=PostSerializer(instance=post)
#     if post:
#         return Response(data=serializer.data,status=200)
#     return Response(data={"message":"Post not found"},status=404)





# @api_view(http_method_names=["PATCH"])
# @permission_classes([IsAuthenticated])
# @swagger_auto_schema(operation_description="Update a post",request_body=PostSerializer,responses={200:PostSerializer})
# def update_post(request,post_id:uuid.UUID):
#     post=get_object_or_404(Post,pk=post_id)
#     serializer=PostSerializer(instance=post)
#     if request.method=="PATCH":
#         data=request.data
#         serializer=PostSerializer(instance=post,data=data,partial=True,context={"request":request})
#         if serializer.is_valid():
#             serializer.save()
#             res={
#                 "msg":"Post updated successfully",
#                 "data":serializer.data
#             }
#             return Response(data=res,status=200)
#         return Response(data=serializer.errors,status=400)
#     return Response(data={"message":"Post not found"},status=404)




# @api_view(http_method_names=["DELETE"])
# @permission_classes([IsAuthenticated])
# @swagger_auto_schema(operation_description="Delete a post",responses={204:"Post deleted successfully"})
# def delete_post(request,post_id:uuid.UUID):
#     post=get_object_or_404(Post,pk=post_id)
#     if post:
#         post.delete()
#         return Response(data={"message":"Post deleted successfully"},status=status.HTTP_204_NO_CONTENT)
#     return Response(data={"message":"Post not found"},status=404)



# #############################
# class based API views

class Post_ListCreate(APIView):
    """
    List all posts, or create a new post.
    """
    serializer_class=PostSerializer
    permission_classes=[IsAuthenticated]
    @swagger_auto_schema(operation_description="Get all posts",responses={200:PostSerializer(many=True)})
    def get(self,request:Request,*args,**kwargs):
        posts=Post.objects.all()
        serializer=self.serializer_class(instance=posts,many=True)
        return Response(data=serializer.data,status=200)
    
    @swagger_auto_schema(operation_description="Create a post",request_body=PostSerializer,responses={201:PostSerializer})
    def post(self, request: Request,*args,**kwargs):
        serializer =self.serializer_class(data=request.data,context={"request":request})
        if serializer.is_valid():
            serializer.save()
            res={
                "msg":"Post created successfully",
                "data":serializer.data
            }
            return Response(data=res, status=201)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    


class Post_RetrieveUpdateDestroy(APIView):
    """
    Retrieve, update or delete a post instance.
    """
    serializer_class=PostSerializer
    @swagger_auto_schema(operation_description="Get a single post",responses={200:PostSerializer})
    def get(self,request:Request,post_id:uuid.UUID):
        try:
             post=get_object_or_404(Post,pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"Post not found"})
        serializer=self.serializer_class(instance=post)
        res={
            "msg":"Post retrieved successfully",
            "data":serializer.data
        }
        return Response(data=res,status=200)
    @swagger_auto_schema(operation_description="Update a post",request_body=PostSerializer,responses={200:PostSerializer})
    def patch(self, request:Request, post_id:uuid.UUID):
        try:
            post=get_object_or_404(Post,pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"Post not found"})
        serializer = self.serializer_class(instance=post, data=request.data, partial=True) # partial=True allows for partial updates, not all fields are required
        if serializer.is_valid():
            serializer.save()
            res={
                "msg":"Post updated successfully",
                "data":serializer.data
            }
            return Response(data=res, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(operation_description="Delete a post",responses={204:"Post deleted successfully"})
    def delete(self,request:Request,post_id:uuid.UUID):
        try:
            post=get_object_or_404(Post,pk=post_id)
        except Post.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND,data={"message":"Post not found"})
        post.delete()
        return Response(data={"message":"Post deleted successfully"},status=204)



#Generic API views and Model Mixins
    
"""
The Django REST Framework (DRF) provides a set of generic API views and model mixins
 that allow you to quickly create API endpoints with minimal code.
"""


# class Post_List_Create_View(
#     generics.GenericAPIView,
#     mixins.CreateModelMixin,
#     mixins.ListModelMixin
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer

#     def get(self, request: Request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)

#     def post(self, request: Request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class Post_Retrieve_Update_Destroy_View(
#     generics.GenericAPIView,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     mixins.DestroyModelMixin
# ):
#     queryset = Post.objects.all()
#     serializer_class = PostSerializer
#     lookup_field = 'pk' # the field to use for lookup, default is 'pk' which is the primary key

#     def get(self, request: Request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def patch(self, request: Request, *args, **kwargs):
#         return self.update(request, *args, **kwargs)

#     def delete(self, request: Request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)



#viewsets and routers
    
"""
Viewsets and routers are another way to create API endpoints in DRF.
Viewsets are classes that provide CRUD operations for a model or queryset.
Routers are used to automatically create URL patterns for viewsets.
"""


#all crud operations can be done with a viewset
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'