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
from datetime import datetime

viewlog = logging.getLogger("viewlog")


# Home

@api_view(['GET',])
def get_posts(request):

    print(request.user)
    posts = [p.to_dict() for p in Post.objects.all()]
    viewlog.debug(f"{request.path}: All Posts {posts}")
    return Response(posts, status=status.HTTP_200_OK)

# Creating,Updating & Deleting Posts

@api_view(['POST'])
@permission_classes([IsAuthenticated,])  
def post_create_view(request,*args,**kwargs):

    post = Post()
    post.author = request.user.profile
    post.title = request.data["title"]
    post.content = request.data['content']
    post.save()

    viewlog.debug(f"{request.path}: New Post {post.to_dict()}")
    return Response(post.to_dict(), status=status.HTTP_201_CREATED)

@api_view(['GET',])  
def post_detail_view(request,id):

    post = Post()
    
    try:
        post = Post.objects.get(pk=id)
    except post.DoesNotExist:
        return Response("Post not found", status=status.HTTP_404_NOT_FOUND)

    if Comment.objects.filter(post_id=id).count():
        comments = Comment()
        comments = [c.to_dict() for c in Comment.objects.filter(post_id=id)]
        return Response([post.to_dict(),comments], status=status.HTTP_200_OK)
    else:
        return Response([post.to_dict()], status=status.HTTP_200_OK)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])  
def post_update_view(request,id,*args,**kwargs):

    post = Post.objects.get(id=id)

    if request.user.profile == post.author:
        post.author = request.user.profile
        post.title = request.data["title"]
        post.content = request.data["content"]
        post.save()

    viewlog.debug(f"{request.path}: Updated Post {post.to_dict()}")
    return Response(post.to_dict(), status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated,])  
def post_report_view(request,id,*args,**kwargs):

    post = Post.objects.get(id=id)

    if request.user.profile != post.author:
        if request.user.profile not in post.reported_by.all():
            post.reported_by.add(request.user.profile)
            post.save()
            if post.reported_by.count() > 4:
                messages.warning(
                    request, f'Post "{post.title}" has been successfully deleted.'
                )
                post.delete() 
                return Response(status=status.HTTP_204_NO_CONTENT) 
            else:
                return Response(status=status.HTTP_200_OK)
    else:
        return Response(status=status.HTTP_403_FORBIDDEN)            

@api_view(['POST',])  
def post_delete_view(request,id):

    post = Post()

    try:
        post = Post.objects.get(id=id)
        if request.user.profile == post.author:
            post.delete() 
    except post.DoesNotExist:
        return Response("Post not found", status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)    

# Creating,Updating & Deleting Comments

@api_view(['GET',])
def get_comments(request,id):

    print(request.user)
    if Comment.objects.filter(post_id=id).count() != 0:
        comments = [c.to_dict() for c in Comment.objects.filter(post_id=id)]
        viewlog.debug(f"{request.path}: All Comments {comments}")
        return Response(comments, status=status.HTTP_200_OK)
    else:    
        return Response(comments, status=status.HTTP_404_NOT_FOUND)
    

@api_view(['POST',])
@permission_classes([IsAuthenticated,])  
def comment_create_view(request,id):

    print(request.data)
    post = Post.objects.get(id=id)
    comment = Comment(post=post)
    comment.author = request.user.profile
    comment.post_id = id
    comment.content = request.data["comment"]
    comment.save()
    
    viewlog.debug(f"{request.path}: New Comment {comment.to_dict()}")
    return Response(comment.to_dict(), status=status.HTTP_201_CREATED)    

@api_view(['POST'])
@permission_classes([IsAuthenticated,])  
def comment_update_view(request,id,comment_id):

    post = Post.objects.get(id=id)
    comment = Comment.objects.get(id=comment_id)
    if request.user.profile == comment.author:
        comment.author = request.user.profile
        comment.post_id = id
        comment.content = request.data["comment"]
        comment.save()
    
    viewlog.debug(f"{request.path}: Comment {comment.to_dict()} has been updated")
    return Response(comment.to_dict(), status=status.HTTP_200_OK)    


@permission_classes([IsAuthenticated,])  
@api_view(['POST',])  
def comment_delete_view(request,id,comment_id):
    comment = Comment()
    try:
        post = Post.objects.get(id=id)
        comment = Comment.objects.get(id=comment_id)
        if request.user.profile == comment.author:
            comment.delete() 
    except post.DoesNotExist and comment.DoesNotExist :
        return Response("Comment not found", status=status.HTTP_404_NOT_FOUND)

    return Response(status=status.HTTP_204_NO_CONTENT)    