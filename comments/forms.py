from django import forms

class commentform(forms.Form):
	content=forms.CharField(label="",widget=forms.Textarea)