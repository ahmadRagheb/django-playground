from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
# Create your models here.
from .vaidatiors import validate_author_email,validate_justin

PUBLISH_CHOICES = [
		('draft','Draft'),
		('publish','Publish'),
		('private','Private'),		
	]

class PostModel(models.Model):
	id 				= models.BigAutoField(primary_key=True)
	active 			= models.BooleanField(default=True)
	title			= models.CharField(max_length=240, verbose_name='Post title', unique=True)
	content			= models.TextField(null=True,blank=True)
	publish 		= models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
	view_count		= models.IntegerField(default=0)
	publish_date	= models.DateField(auto_now=False, auto_now_add=False, default=timezone)
	author_email 	= models.EmailField(max_length=240, vaidatiors=[validate_author_email,validate_justin],
										null=True, blank=True)

	class meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'			
		# unique_together = [('title','slug')]

	#smart_text method for unicode whatever language we are using no errors
	def __unicode__(self): #python 2
		return smart_text(self.title)

	def __str__(self): #python 3
		return smart_text(self.title)