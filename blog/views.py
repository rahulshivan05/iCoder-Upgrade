from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.core.exceptions import PermissionDenied
from blog.models import Post, BlogComment
import json
from django.http import JsonResponse
from django.utils.translation import activate
from django.urls import reverse
from django.contrib import messages
from blog.templatetags import extras
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def blogHome(request):
	allPosts = Post.objects.all()
	context = {'allPosts': allPosts}
	return render(request, 'blog/blogHome.html', context)

def blogPost(request, slug):
	post = Post.objects.filter(slug=slug).first()  # "[0]"
	post.views = post.views + 1
	post.save()
	comment = BlogComment.objects.filter(post=post, parent=None)
	replies = BlogComment.objects.filter(post=post).exclude(parent=None)
	replyDict = {}
	for reply in replies:
		if reply.parent.sno not in replyDict.keys():
			replyDict[reply.parent.sno] = [reply]
		else:
			replyDict[reply.parent.sno].append(reply)		
	# print(comment, replies)		
	context = {'post': post, 'comment': comment, 'user': request.user, 'replyDict': replyDict}
	return render(request, 'blog/blogPost.html', context)

# @login_required(login_url='/accounts/login/')
def postComment(request):
	if request.method == "POST":
		comment = request.POST.get("comment")
		user = request.user
		postSno = request.POST.get("postSno")
		post = Post.objects.get(sno=postSno)
		parentSno = request.POST.get("parentSno")

		if parentSno == "":
			comment = BlogComment(comment=comment, user=user, post=post)
			comment.save()
			messages.success(request, "Your Comment has been Posted Successfully.")
		else:
			parent = BlogComment.objects.get(sno=parentSno)
			comment = BlogComment(comment=comment, user=user, post=post, parent=parent)

			comment.save()
			messages.success(request, "Your Replay has been Posted Successfully.")

	return redirect(f"/blog/{post.slug}")
