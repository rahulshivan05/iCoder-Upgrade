
from django.urls import path, include

from .  import views

urlpatterns = [
	# API for post a comment
    path('postComment', views.postComment, name="postComment"),
    
    path('', views.blogHome, name='blogHome'),
    path('<str:slug>', views.blogPost, name='blogPost'),

]