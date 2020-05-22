from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string
from ..models import Item, List
from ..views import home_page
from lists.forms import ItemForm, EMPTY_ITEM_ERROR
from unittest import skip
import re

# Create your tests here.


# Removes csrf_token to be able to compare
# @staticmethod
def remove_csrf(html_code):
    csrf_regex = r'<input[^>]+csrfmiddlewaretoken[^>]+>'
    return re.sub(csrf_regex, '', html_code)


class HomePageTest(TestCase):

	def test_root_url_resolves_to_home_page_view(self):
		found = resolve('/')
		self.assertEqual(found.func, home_page)

	def test_home_page_returns_correct_html(self):
		request = HttpRequest()
		response = home_page(request)

		expected_html = render_to_string(
			'lists/home.html',
			request=request,
			context={'form': ItemForm()}

		)
		# decode() to convert response.content bytes into a Python
		# unicode string, making it able to compare with another string
		# csrf_token needs to be removed for comparison
		self.assertEqual(
			remove_csrf(response.content.decode()),
			remove_csrf(expected_html)
		)

	def test_home_page_uses_item_form(self):
		response = self.client.get('/')
		self.assertIsInstance(response.context['form'], ItemForm)


class ListViewTest(TestCase):

	def test_uses_list_templates(self):
		list_ = List.objects.create()
		response = self.client.get('/lists/%d/' % (list_.id))
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_display_only_items_for_that_list(self):

		correct_list = List.objects.create()
		for x in range(1, 5):
			# list_ = List.objects.create()
			text = 'itemey ' + str(x)
			Item.objects.create(text=text, list=correct_list)

		other_list = List.objects.create()
		for x in range(1, 5):
			# list_ = List.objects.create()
			text = 'other list item ' + str(x)
			Item.objects.create(text=text, list=other_list)

		response = self.client.get('/lists/%d/' % (correct_list.id))

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 3')
		self.assertNotContains(response, 'other list item 1')
		self.assertNotContains(response, 'other list item 2')

	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get('/lists/%d/' % (correct_list.id,))
		self.assertEqual(response.context['list'], correct_list)

	def test_can_save_a_POST_request_to_an_existing_list(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		self.client.post(
			'/lists/%d/' % (correct_list.id, ),
			data={'text': 'A new item for an existing list'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)

	def test_POST_redirects_to_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()

		response = self.client.post(
			'/lists/%d/' % (correct_list.id,),
			data={'text': 'A new item for an existing list'}
		)
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

	def post_invalid_input(self):
		list_ = List.objects.create()
		return self.client.post(f'/lists/{list_.id}/', data={'text': ''})

	def test_for_invalid_input_nothing_saved_to_db(self):
		self.post_invalid_input()
		self.assertEqual(Item.objects.count(), 0)

	def test_for_invalid_input_renders_list_template(self):
		response = self.post_invalid_input()
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.post_invalid_input()
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_for_invalid_input_shows_error_on_page(self):
		response = self.post_invalid_input()
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_displays_item_form(self):
		list_ = List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertIsInstance(response.context['form'], ItemForm)
		self.assertContains(response, 'name="text"')

	@skip
	def test_duplicate_item_validation_errors_end_up_on_lists_page(self):
		list1 = List.objects.create()
		item1 = Item.objects.create(list=list1, text='textou')
		response = self.client.post(
			f'/lists/{list1.id}/',
			data={'text': 'textou'}
		)

		expected_error = escape("You've already got this on your list")
		self.assertContains(response, expected_error)
		self.assertTemplateUsed(response, 'lists/list.html')
		self.assertEqual(Item.objects.all().count(), 1)


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'text': 'A new list item'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'text': 'A new list item'}
		)
		new_list = List.objects.first()
		# redirect has status code 302
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

	def test_for_invalid_input_renders_home_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/home.html')

	def test_validation_errors_are_shown_on_home_page(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertContains(response, escape(EMPTY_ITEM_ERROR))

	def test_for_invalid_input_passes_form_to_template(self):
		response = self.client.post('/lists/new', data={'text': ''})
		self.assertIsInstance(response.context['form'], ItemForm)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
