from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.utils.html import escape
from django.template.loader import render_to_string
from ..models import Item, List
from ..views import home_page
from lists.forms import ItemForm
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
			# {'new_item_text': 'A new list item'},
			request=request,
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
			data={'item_text': 'A new item for an existing list'}
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
			data={'item_text': 'A new item for an existing list'}
		)
		self.assertRedirects(response, '/lists/%d/' % (correct_list.id,))

	def test_validation_errors_end_up_on_lists_page(self):
		list_ = List.objects.create()

		response = self.client.post(
			f'/lists/{list_.id}/',
			data={'item_text': ''}
		)
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/list.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)


class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)

		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)
		new_list = List.objects.first()
		# redirect has status code 302
		self.assertRedirects(response, '/lists/%d/' % (new_list.id,))

	def test_validation_errors_are_sent_back_to_home_page_template(self):
		response = self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(response.status_code, 200)
		self.assertTemplateUsed(response, 'lists/home.html')
		expected_error = escape("You can't have an empty list item")
		self.assertContains(response, expected_error)

	def test_invalid_list_items_arent_saved(self):
		self.client.post('/lists/new', data={'item_text': ''})
		self.assertEqual(List.objects.count(), 0)
		self.assertEqual(Item.objects.count(), 0)
