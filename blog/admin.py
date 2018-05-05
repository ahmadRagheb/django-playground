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
		'timestamp'
	]

	"""add updated and timestamp to readonly fields 
		so we can see them in admin without problem """

	readonly_fields = ['updated','timestamp','new_content']

	#create new field not in database to be showed in admin as read only field
	def new_content(self, obj, *args, **kwargs):
		return str(obj.title)

	class Meta:
		model = PostModel
		
admin.site.register(PostModel,PostModelAdmin)