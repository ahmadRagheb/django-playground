from django.db import models
# Create your models here.

class PostModel(models.Model):
	id 			= models.BigAutoField(primary_key=True)
	active 		= models.BooleanField(default=True)
	title		= models.CharField(max_length=240)
	content		= models.TextField(null=True,blank=True)


	pass