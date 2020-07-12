from django.urls import path
from . import views

urlpatterns = [
    path('api/posts/', views.get_posts, name='get-posts'),
    path('api/post/new/', views.post_create_view, name='post-create'),
    path('api/post/<int:id>/',views.post_detail_view,name='post-detail'),
    path('api/post/<int:id>/update/', views.post_update_view, name='post-update'),
    path('api/post/<int:id>/report/', views.post_report_view, name='post-report'),
    path('api/post/<int:id>/delete/', views.post_delete_view, name='post-delete'),
    path('api/post/<int:id>/comments/', views.get_comments, name = 'get-comments'),
    path('api/post/<int:id>/comment/new/', views.comment_create_view, name = 'comment-create'),
    path('api/post/<int:id>/comment/<int:comment_id>/update/', views.comment_update_view, name = 'comment-update'),
    path('api/post/<int:id>/comment/<int:comment_id>/delete/', views.comment_delete_view, name = 'comment-delete'),
]
