from django.db import models
from django.urls import reverse
from django.conf import settings
# Create your models here.


class List(models.Model):

	owner = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True,
		on_delete=models.CASCADE)
<<<<<<< HEAD
=======
	#  the @property decorator transforms a method on a class to make it appear to the outside
	# world like an attribute.
	@property
	def name(self):
		return self.item_set.first().text
>>>>>>> 2713d1dec2846f734cf206da6bd6aada93331cf2

	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

	@staticmethod
	def create_new(first_item_text, owner=None):
		list_ = List.objects.create(owner=owner)
		Item.objects.create(text=first_item_text, list=list_)
		return list_

	@property
	def name(self):
		return self.item_set.first().text


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
