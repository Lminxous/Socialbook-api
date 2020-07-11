# Models
from .models import Post,Comment
from django.contrib.auth.models import User
# Rest Framework
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
# Other 
import logging
import sys

viewlog = logging.getLogger("viewlog")


# Home

@api_view(['GET',])
def get_posts(request):

    print(request.user)
    posts = [p.to_dict() for p in Post.objects.all()]
    viewlog.debug(f"{request.path}: All Posts {posts}")
    return Response(posts, status=status.HTTP_200_OK)

# Creating,Updating & Deleting Posts

@api_view(['POST',])
@permission_classes([IsAuthenticated,])  
def post_create_view(request):

    json_data = request.data

    post = Post()
    post.author = request.user
    post.title = json_data["title"]
    post.content = json_data["content"]
    post.date_posted = datetime.datetime.fromisoformat(json_data["date_posted"])
    post.reported_by = datetime.datetime.fromisoformat(json_data["reported_by"])
    post.save()

    viewlog.debug(f"{request.path}: New Post {post.to_dict()}")
    return Response(post.to_dict(), status=status.HTTP_201_CREATED)

@api_view(['GET',])  
def post_detail_view(request,id):

    post = Post()

    try:
        post = Post.objects.get(id=id)
        comments = Comment.objects.get(post_id=id)
    except post.DoesNotExist:
        return Response("Post not found", status=status.HTTP_404_NOT_FOUND)

    return Response([post.to_dict(),comments.to_dict()], status=status.HTTP_200_OK)

@api_view(['PUT',])
@permission_classes([IsAuthenticated,])  
def post_update_view(request,id):

    json_data = request.data
    post = Post.objects.get(post_id=id)

    if request.user == post.author:
        post.author = request.user
        post.title = json_data["title"]
        post.content = json_data["content"]
        post.date_posted = datetime.datetime.fromisoformat(json_data["date_posted"])
        post.reported_by = datetime.datetime.fromisoformat(json_data["reported_by"])
        post.save()

    viewlog.debug(f"{request.path}: New Post {post.to_dict()}")
    return Response(post.to_dict(), status=status.HTTP_201_CREATED)


@api_view(['POST',])  
def post_delete_view(request,id):

    post = Post()

    try:
        post = Post.objects.get(id=id)
        if request.user == post.author:
            post.delete() 
    except post.DoesNotExist:
        return Response("Post not found", status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)    

# Creating,Updating & Deleting Comments

@api_view(['POST',])
@permission_classes([IsAuthenticated,])  
def comment_create_view(request):

    json_data = request.data
    comment = Comment()
    comment.author = request.user
    comment.post = json_data["post"]
    comment.content = json_data["content"]
    comment.save()
    
    viewlog.debug(f"{request.path}: New Comment {comment.to_dict()}")
    return Response(comment.to_dict(), status=status.HTTP_201_CREATED)    

@api_view(['PUT',])
@permission_classes([IsAuthenticated,])  
def comment_update_view(request,id):

    json_data = request.data
    comment = Comment.objects.get(comment_id=id)
    if request.user == comment.author:
        comment.author = request.user
        comment.post = json_data["post"]
        comment.content = json_data["content"]
        comment.save()
    
    viewlog.debug(f"{request.path}: Comment {comment.to_dict()} has been updated")
    return Response(comment.to_dict(), status=status.HTTP_200_OK)    


@permission_classes([IsAuthenticated,])  
@api_view(['POST',])  
def comment_delete_view(request,id):
    comment = Comment()
    try:
        comment = Comment.objects.get(comment_id=id)
        if request.user == comment.author:
            comment.delete() 
    except post.DoesNotExist:
        return Response("Comment not found", status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)    