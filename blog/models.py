from django.db import models
from django.utils.encoding import smart_text
# Create your models here.

PUBLISH_CHOICES = [
		('draft','Draft'),
		('publish','Publish'),
		('private','Private'),		
	]

class PostModel(models.Model):
	id 			= models.BigAutoField(primary_key=True)
	active 		= models.BooleanField(default=True)
	title		= models.CharField(max_length=240, verbose_name='Post title')
	content		= models.TextField(null=True,blank=True)
	publish 	= models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
	class meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'			

	#smart_text method for unicode whatever language we are using no errors
	
	def __unicode__(self): #python 2
		return smart_text(self.title)

	def __str__(self): #python 3
		return smart_text(self.title)