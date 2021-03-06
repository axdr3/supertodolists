from django import forms
from .models import Item, List
from django.core.exceptions import ValidationError

EMPTY_ITEM_ERROR = "You can't have an empty list item"
DUPLICATE_ITEM_ERROR = "You've already got this on your list"


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
	# but this is the neatest I think.



"""

The form to create a new list only needs to know one thing, the new item text. A form which validates
that list items are unique, needs to know the list too. Just as we overrode the save method on our ItemForm,
this time we’ll override the constructor on our new form class so that it knows what list it applies to.

"""

# TODO:IMPROVE merge it with ItemForm?


class ExistingListItemForm(ItemForm):

	# That’s a bit of Django voodoo right there, but we basically take the validation error,
	# adjust its error message, and then pass it back into the form.
	def __init__(self, for_list, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.instance.list = for_list

	def validate_unique(self):
		try:
			self.instance.validate_unique()
		except ValidationError as e:
			e.error_dict = {'text': [DUPLICATE_ITEM_ERROR]}
			self._update_errors(e)


class NewListForm(ItemForm):

	def save(self, owner):
		print(f'Owner is is_authenticated {owner.is_authenticated}')
		print(f'Owner {owner}')
		if owner.is_authenticated:
			return List.create_new(first_item_text=self.cleaned_data['text'], owner=owner)
		else:
			return List.create_new(first_item_text=self.cleaned_data['text'])
