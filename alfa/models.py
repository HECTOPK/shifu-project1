from django.db import models
from ckeditor_uploader.fields import RichTextUploadingField

class Article(models.Model):
	title = models.CharField(max_length = 500, default = '')
	image = models.ImageField(upload_to='img/', blank=False)
	content = RichTextUploadingField(blank=False, null=True)
	preview_text =  models.CharField(max_length = 500, default = '')
	datetime = models.DateTimeField(auto_now=True)
	class Meta:
		ordering = ['-datetime']
