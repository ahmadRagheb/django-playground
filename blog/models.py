from django.db import models
# Create your models here.

class PostModel(models.Model):
	id 			= models.BigAutoField(primary_key=True)
	active 		= models.BooleanField(default=True)
	title		= models.CharField(max_length=240, verbose_name='Post title')
	content		= models.TextField(null=True,blank=True)

	class meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'			