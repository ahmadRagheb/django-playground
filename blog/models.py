from datetime import timedelta, datetime, date
from django.db import models
from django.utils.encoding import smart_text
from django.utils import timezone
from django.utils.text import slugify
from django.utils.timesince import timesince

from django.db.models.signals import post_save,pre_save,post_delete
# Create your models here.


from .validators import validate_author_email,validate_justin

PUBLISH_CHOICES = [
		('draft','Draft'),
		('publish','Publish'),
		('private','Private'),		
	]

""" Custom QuerySet Methods """
class PostModelQuerySet(models.query.QuerySet):
	def active(self):
		return self.filter(active=True)

	def post_title_items(self,value):
		return self.filter(title__icontains=value)


""" Model Mangers """
class PostModelManager(models.Manager):
	"""docstring for PostModelManager"""
	def get_queryset(self):
		return PostModelQuerySet(self.model, using=self._db)

	def all(self, *args, **kwargs):
		# qs = super(PostModelManager, self).all(*args, **kwargs).filter(active=True)
		qs = self.get_queryset().active()
		return qs

	def get_timeframe(self, date1, date2):
		# assume datetime objects 
		qs = self.get_queryset()
		qs_time_1 = qs.filter(publish_date__gte=date1)
		qs_time_2 = qs_time_1.filter(publish_date__lt=date2)
		# final_qs  = (qs_time_1 | qs_time_2).distinct()
		return qs_time_2		

class PostModel(models.Model):
	id 				= models.BigAutoField(primary_key=True)
	active 			= models.BooleanField(default=True)
	title			= models.CharField(
							max_length=240,
							verbose_name='Post title',
							unique=True,
							error_messages={
								"unique":"This title is not unique , please try again",
								"blank":"This field is not full, please try again"		
							},
							help_text='Must be a unique title.')
	slug 			= models.SlugField(null=True, blank=True)
	content			= models.TextField(null=True,blank=True)
	publish 		= models.CharField(max_length=120, choices=PUBLISH_CHOICES, default='draft')
	view_count		= models.IntegerField(default=0)
	publish_date	= models.DateField(auto_now=False, auto_now_add=False, default = timezone.now)
	author_email 	= models.EmailField(max_length=240, validators=[validate_author_email,validate_justin],
										null=True, blank=True)
	#when it's updated
	updated 		= models.DateTimeField(auto_now=True)
	#when it's inserted to db
	timestamp  		= models.DateTimeField(auto_now_add=True)
	objects 		= PostModelManager()


	#overriding save method 
	def save(self,*args,**kwargs):
		if not self.slug and self.title:
			self.slug = slugify(self.title)
		super(PostModel,self).save(*args,**kwargs)


	class meta:
		verbose_name = 'Post'
		verbose_name_plural = 'Posts'			
		# unique_together = [('title','slug')]

	#smart_text method for unicode whatever language we are using no errors
	def __unicode__(self): #python 2
		return smart_text(self.title)

	def __str__(self): #python 3
		return smart_text(self.title)

	# Instance Methode 
	@property 
	def age(self):
		if self.publish == 'publish':
			now = datetime.now()
			publish_time = datetime.combine(
								self.publish_date,
								datetime.min.time()
						)
			try:
				difference = now - publish_time
			except:
				return "Unknown"
			if difference <= timedelta(minutes=1):
				return "just now"
			else:
				time=timesince(publish_time).split(', ')[0]
				return time

		return "Not published"

#signals Before save 
def blog_post_model_pre_save_receiver(sender, instance, *args, **kwargs):
	if not instance.slug and instance.title:
		instance.slug = slugify(instance.title)

pre_save.connect(blog_post_model_pre_save_receiver, sender=PostModel)


#signals After save 
def blog_post_model_post_save_receiver(sender, instance, created, *args, **kwargs):
	if created:
		if not instance.slug and instance.title:
			instance.slug = slugify(instance.title)
			instance.save()

post_save.connect(blog_post_model_post_save_receiver, sender=PostModel)


#signals Before delete 
def blog_post_model_post_delete_receiver(sender, instance, *args, **kwargs):
	print("After delete")

post_delete.connect(blog_post_model_post_delete_receiver, sender=PostModel)

