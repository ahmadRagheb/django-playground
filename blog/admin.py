from django.contrib import admin

# Register your models here.

from .models import PostModel


class PostModelAdmin(admin.ModelAdmin):
	#override the admin to show specific fields 
	fields = [
		'title',
		'slug',
		'content',
		'publish',
		'publish_date',
		'active',
		'updated',
		'timestamp',
		'get_age'
	]

	"""add updated and timestamp to readonly fields 
		so we can see them in admin without problem """

	readonly_fields = ['updated','timestamp','get_age']

	#create new field not in database to be showed in admin as read only field
	def get_age(self, obj, *args, **kwargs):
		return obj.age

	class Meta:
		model = PostModel
		
admin.site.register(PostModel,PostModelAdmin)