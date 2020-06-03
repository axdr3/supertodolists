from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.


class List(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
		on_delete=models.CASCADE)
	#  the @property decorator transforms a method on a class to make it appear to the outside
	# world like an attribute.
	@property
	def name(self):
		return self.item_set.first().text

	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])


class Item(models.Model):
	text = models.TextField(default='')
	list = models.ForeignKey(List, blank=True, null=True, on_delete=models.CASCADE)

	# Just like ModelForms, models have a class Meta, and that’s where we can implement
	# a constraint which says that an item must be unique for a particular list, or in
	# other words, that text and list must be unique together

	class Meta:
		ordering = ('id',)
		unique_together = ('list', 'text')

	def __str__(self):
		return self.text
