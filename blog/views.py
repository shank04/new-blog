from django.shortcuts import render,get_object_or_404,redirect
from django.contrib import messages
from django.db.models import Q
# Create your views here.
from .models import Post
from .forms import Postform
from django.http import HttpResponseRedirect,Http404,HttpResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from comments.models import Comment
from comments.forms import commentform
from django.contrib.auth import authenticate,login
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views import generic
from django.views.generic import View
from .forms import UserForm
from .forms import LoginForm


def post_list(request):
	posts=Post.objects.all()
	if request.user.is_authenticated():

		selfposts=Post.objects.filter(user=request.user)

	query=request.GET.get('q')
	if query:
		posts=posts.filter(Q(title__icontains=query)|Q(content__contains=query))

	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
		    
	try:
		post_page = paginator.page(page)
	except PageNotAnInteger:
		        # If page is not an integer, deiver first page.
		post_page = paginator.page(1)
	except EmptyPage:
		        # If page is out of range (e.g. 9999), deliver last page of results.
		post_page = paginator.page(paginator.num_pages)
	if request.user.is_authenticated():

		context={
			'posts':posts,
			'post_page':post_page,

			'selfposts':selfposts
		}
	else:
		context={
			'posts':posts,
			'post_page':post_page,

			
		}

	return render(request,'post_list.html',context)
		

def post_detail(request,id):
	instance=get_object_or_404(Post,id=id)
	if request.user.is_authenticated():

		selfposts=Post.objects.filter(user=request.user)

	c=Comment.objects.filter(post__id=id)
	
	form=commentform(request.POST or None)
	if form.is_valid():
		if(request.user.is_authenticated()==False):
			response=HttpResponse("<h3>Sorry, You need to be logged in to post a comment</h3>")
			response.status_code=403
			return response

		content_data=form.cleaned_data.get("content")
		new_comment, created=Comment.objects.get_or_create(
			user=request.user,
			post=instance,
			content=content_data,
			)
		return HttpResponseRedirect(new_comment.post.get_absolute_url())
	if request.user.is_authenticated():

		context={
		'instance':instance,
		'comments':c,
		'comment_form':form,
		'selfposts':selfposts
		}
	else:
		context={
		'instance':instance,
		'comments':c,
		'comment_form':form,
		
		}

	return render(request,'post_detail.html',context)

# @login_required(login_url='/login/')
def post_create(request):
	if(request.user.is_authenticated()==False):
			response=HttpResponse("<h3>Sorry, You need to be logged in to write a Blog</h3>")
			response.status_code=403
			return response
	selfposts=Post.objects.filter(user=request.user)

	inst=Post(user=request.user)
	form=Postform(request.POST or None,request.FILES or None,instance=inst,)
	if form.is_valid():
		instance=form.save(commit=False)
		instance.save()
		messages.success(request,'Successfully Posted')
		return HttpResponseRedirect(instance.get_absolute_url())
	
	context={'form':form,'selfposts':selfposts}
	return render(request,'post_form.html',context)

def post_update(request,id):
	instance=get_object_or_404(Post,id=id)
	if(instance.user!=request.user):
		# raise Http404
		response=HttpResponse("<h3>Sorry, You do not have permissions to do this</h3>")
		response.status_code=403
		return response
	form=Postform(request.POST or None,request.FILES or None,instance=instance)
	if form.is_valid():
			instance=form.save(commit=False)
			instance.save()
			messages.success(request,'Your Post has been Updated')

			return HttpResponseRedirect(instance.get_absolute_url())

	context={
		'instance':instance,
		'form':form
	}
	return render(request,'post_form.html',context)

def post_delete(request,id):
	instance=get_object_or_404(Post,id=id)
	if(instance.user!=request.user):
		# messages.success(request,"try")
		# raise Http404
		response=HttpResponse("<h3>Sorry, You do not have permissions to do this</h3>")
		response.status_code=403
		return response

	if (request.method=='POST'):

		instance.delete()
		messages.success(request,'Your Post has been Deleted')
		return HttpResponseRedirect('http://127.0.0.1:8000/posts/')

	context={
		'instance':instance,
		
	}
	
	return render(request,'post_delete.html',context)
	


def UserFormView(request):
	form=UserForm(request.POST or None)
	if form.is_valid():
		user=form.save(commit=False)

		username=form.cleaned_data.get('username')
		password=form.cleaned_data.get('password')
			# profile_pic=form.cleaned_data['profile_pic']
		user.set_password(password)
			
		user.save()
		user=authenticate(username=username,password=password)
		login(request,user)
		messages.success(request,'You are Successfully Registered:)')

		return redirect('post_list')
	return render(request,'registration-form.html',{'form':form})


def LoginFormView(request):
	# form_class=LoginForm
	# template_name='login-form.html'
	form=LoginForm(request.POST or None)
	if form.is_valid():
		username=form.cleaned_data.get("username")
		password=form.cleaned_data.get("password")
		user=authenticate(username=username,password=password)
		login(request,user)
		messages.success(request,'You are logged in!')
		return redirect('post_list')
	return render(request,'login-form.html',{'form':form})



@login_required
def user_logout(request):
	if(request.method=='POST'):
   
		logout(request)
		messages.success(request,'You are Logged out. Be back soon!')
		return redirect('post_list')
	return render(request,'logout.html')


def myposts(request):
	if not request.user.is_authenticated():
		response=HttpResponse("<h3>Sorry, You need to logged in to view this section</h3>")
		response.status_code=403
		return response

	posts=Post.objects.filter(user=request.user)
	query=request.GET.get('q')
	if query:
		posts=posts.filter(Q(title__icontains=query)|Q(content__contains=query))

	paginator = Paginator(posts, 5)
	page = request.GET.get('page')
		    
	try:
		post_page = paginator.page(page)
	except PageNotAnInteger:
		        # If page is not an integer, deiver first page.
		post_page = paginator.page(1)
	except EmptyPage:
		        # If page is out of range (e.g. 9999), deliver last page of results.
		post_page = paginator.page(paginator.num_pages)

	context={
	'posts':posts,
	'post_page':post_page,
	}
	return render(request,'myposts.html',context)
