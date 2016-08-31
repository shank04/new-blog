from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login



class Postform(forms.ModelForm):
	published_date=forms.DateTimeField(widget=forms.SelectDateWidget)
	content=forms.CharField(widget=PagedownWidget)
	class Meta:
		model=Post
		fields=['user','title','content','image','published_date']


class UserForm(forms.ModelForm):
	password=forms.CharField(widget=forms.PasswordInput)
	password2=forms.CharField(label='Confirm password',widget=forms.PasswordInput)

	# profile_pic=forms.ImageField(required=False)
	class Meta:
		model=User
		fields=['username','email','password','password2']


	def clean_password2(self):
		password=self.cleaned_data.get("password")
		password2=self.cleaned_data.get("password2")
		if password2!=password:
			raise forms.ValidationError("Passwords must match")
		return password



class LoginForm(forms.Form):
	username=forms.CharField()
	password=forms.CharField(widget=forms.PasswordInput)

	
	def clean(self,*args,**kwargs):
		username=self.cleaned_data.get("username")
		password=self.cleaned_data.get("password")
		if username and password:
			user=authenticate(username=username,password=password)
			# if not user.check_password(password):
			# 	raise forms.ValidationError("Incorrect Password")
			

			if not user:
				raise forms.ValidationError("Either username or password is incorrect")
			if not user.is_active:
				raise forms.ValidationError("This user is no longer active")
		return super(LoginForm,self).clean(*args,**kwargs)



