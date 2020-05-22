from django import forms
from .models import Item

EMPTY_ITEM_ERROR = "You can't have an empty list item"


class ItemForm(forms.models.ModelForm):

	class Meta:
		model = Item
		fields = ('text',)
		widgets = {
			'text': forms.fields.TextInput(attrs={
				'placeholder': 'Enter a to-do item',
				'class': 'form-control form-control-lg',
				}),
		}
		error_messages = {
			'text': {'required': EMPTY_ITEM_ERROR}
		}

	# The .instance attribute on a form represents the database
	# object that is being modified or created. There are other ways of getting this to work,
	# including manually creating the object yourself, or using the commit=False argument to save,
	# but this is the neatest I think. We’ll explore a different way of making a form "know" what
	# list it’s for in the next chapter:
	def save(self, for_list):
		self.instance.list = for_list
		return super().save()
