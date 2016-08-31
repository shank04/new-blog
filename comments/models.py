from __future__ import unicode_literals

from django.db import models

# Create your models here.
from django.conf import settings
from blog.models import Post

class Comment(models.Model):
	user=models.ForeignKey(settings.AUTH_USER_MODEL,default=1)
	post=models.ForeignKey(Post,null=True)
	content=models.TextField(null=True)
	timestamp=models.DateTimeField(auto_now_add=True)


	def __unicode__(self):
		return str(self.content)

	def __str__(self):
		return str(self.content)

	class Meta:
		ordering=["-timestamp"]