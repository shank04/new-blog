from __future__ import unicode_literals

from django.db import models
from django.core.urlresolvers import reverse
# Create your models here.
from django.conf import settings

def upload_location(instance,filename):
	return "%s/%s" %(instance.id,filename)


class Post(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	title=models.CharField(max_length=20)
	content=models.TextField()
	image=models.ImageField(null=True, blank=True, upload_to=upload_location,)
	updated_date=models.DateTimeField(auto_now=True,auto_now_add=False)
	published_date=models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.title

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('post_detail',kwargs={"id":self.id})

	class Meta:
		ordering=['-published_date','-updated_date']
