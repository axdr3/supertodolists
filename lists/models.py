from django.db import models
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db.models.signals import m2m_changed
from django.shortcuts import redirect
User = get_user_model()
# Create your models here.



class List(models.Model):
	# pass

	owner = models.ForeignKey(User, blank=True, null=True,
		on_delete=models.CASCADE)

	shared_with = models.ManyToManyField(User,
		related_name='sharees')

	def get_absolute_url(self):
		return reverse('view_list', args=[self.id])

	@staticmethod
	def create_new(first_item_text, owner=None):
		list_ = List.objects.create(owner=owner)
		Item.objects.create(text=first_item_text, list=list_)
		return list_

	# the @property decorator transforms a method on a class to make it appear to the outside
	# world like an attribute.

	@property
	def name(self):
		return self.item_set.first().text

# Signal Handler
def shared_with_changed(sender, instance, pk_set, action, **kwargs):
	# instance: the list being modified
	# sender: shared_with
	print(f'Sender {sender}')
	print(f'Action {action}')
	print(f'pk_set {pk_set}')
	print(f'Instance owner {instance.owner.email}')
	if action == 'post_add':
		if instance.owner.email in pk_set:
			print('ERR: cannot add list owner to shared_with')
			sender.delete(instance.owner)

m2m_changed.connect(shared_with_changed, sender=List.shared_with.through)

# end of Handler

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
