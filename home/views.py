from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, Http404
from django.core.exceptions import PermissionDenied
# from django.contrib.postgres.operations import UnaccentExtension
from django.db.models import F
from django.contrib.postgres.aggregates import BoolAnd
from django.contrib.postgres.aggregates import BoolOr
from django.contrib.postgres.constraints import ExclusionConstraint
from django.contrib.postgres.fields import DateTimeRangeField, RangeOperators
from django.contrib.postgres.search import SearchVector

from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from home.models import Contact
from blog.models import Post
from django.contrib import messages

from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required

# Create your views here.

def home(request):
	return render(request, 'home/index.html')


def about(request):
	return render(request, 'home/about.html')


def contact(request):
	if request.method == 'POST':
		name = request.POST['name']
		email = request.POST['email']
		phone = request.POST['phone']
		content = request.POST['content']

		if len(name)<2 or len(email)<3 or len(phone)<10 or len(content)<4:
			messages.error(request, "Please fill the form correctly")
		else:
			contact = Contact(name=name, email=email, phone=phone, content=content)
			contact.save()
			messages.success(request, "Your message has been successfully sent")
	return render(request, 'home/contact.html')


def search(request):
	query = request.GET['query']
	if len(query)>78:
		allPosts = Post.objects.none()
	else:	
		allPostsTitle = Post.objects.filter(title__icontains=query)
		allPostsContent = Post.objects.filter(content__icontains=query)
		allPosts = allPostsTitle.union(allPostsContent)
		# Post.objects.annotate(search=SearchVector('content', 'title'),).filter(search='query')
	
	if allPosts.count() == 0:
		messages.warning(request, "Please input correctly")		
	params = {'allPosts': allPosts, 'query': query}
	return render(request, 'home/search.html', params)

def handleSignup(request):
	if request.method == 'POST':
		username = request.POST['username']
		fname = request.POST['fname']
		lname = request.POST['lname']
		email = request.POST['email']
		pass1 = request.POST['pass1']
		pass2 = request.POST['pass2']

		if len(username) > 10:
			messages.error(request, "Username must be under 10 characters.")
			return redirect('home')

		if not username.isalnum():
			messages.error(request, "Username should only contain letter and numbers.")
			return redirect('home')	

		if pass1 != pass2:
			messages.error(request, "Passwords do not match.")
			return redirect('home')

		# if username.exists():
		# 	messages.error(request, "Username already exixts. Try Another Username")
    # 	username = get_user_model() # your way of getting the User
    # try:
    #     username.objects.get(username__iexact=username)
    # except username.DoesNotExist:
    #     return username
    # raise forms.ValidationError(_("This username has already existed."))	
    	# if User.objects.filter(username=self.cleaned_data['username']).exists():
    	# 	messages.error(request, "Username is Already exixts.")	

    	# if User.objects.filter(username=username).exists():
    		# messages.error(request, "Username is Already exixts")

	    	# Username exists
	    	
	    


		myuser = User.objects.create_user(username, email, pass1)
		myuser.first_name = fname
		myuser.last_name = lname
		myuser.save()
		messages.success(request, "Your iCoder account has been created Successfully created")
		return redirect('/')
	else:
		return HttpResponse('404 Page Not Found')	


# @staff_member_required
def handleLogin(request):
	if request.method == 'POST':
		loginusername = request.POST['loginusername']
		loginpass = request.POST['loginpass']

		user = authenticate(username=loginusername, password=loginpass) 

		if user is not None:
			login(request, user)
			messages.success(request, "Successfully Logged In.")
			return redirect("home")
		else:
			messages.error(request, "invalid credentials. Please try again")
			return redirect('home')	

	return HttpResponse("404 Page Not Found")	



def handleLogout(request):
	logout(request)
	messages.success(request, "Successfully Logged Out!")
	return redirect('home')	



