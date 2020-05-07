from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from .models import Item
from .views import home_page
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

class ItemModelTest(TestCase):
	def test_saving_and_retrieving_items(self):
		first_item = Item()
		first_item.text = 'The first (ever) list item'
		first_item.save()

		second_item = Item()
		second_item.text = 'Item the second'
		second_item.save()

		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(), 2)

		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'The first (ever) list item')
		self.assertEqual(second_saved_item.text, 'Item the second')


class ListViewTest(TestCase):

	def test_uses_list_templates(self):
		response = self.client.get('/lists/the-only-list-in-the-world/')
		self.assertTemplateUsed(response, 'lists/list.html')

	def test_display_all_items(self):

		for x in range(1, 5):
			text = 'itemey ' + str(x)
			Item.objects.create(text=text)

		response = self.client.get('/lists/the-only-list-in-the-world/')

		self.assertContains(response, 'itemey 1')
		self.assertContains(response, 'itemey 3')

class NewListTest(TestCase):
	def test_saving_a_POST_request(self):
		self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)

		# request = HttpRequest()
		# request.method = 'POST'
		# request.POST['item_text'] = 'A new list item'

		# response = home_page(request)

		# TODO: post text too long?
		self.assertEqual(Item.objects.count(), 1)
		new_item = Item.objects.first()
		self.assertEqual(new_item.text, 'A new list item')

	def test_redirects_after_POST(self):
		response = self.client.post(
			'/lists/new',
			data={'item_text': 'A new list item'}
		)

		# redirect has status code 302
		self.assertRedirects(response, '/lists/the-only-list-in-the-world/')
		# self.assertEqual(response.status_code, 302)
		# self.assertEqual(response['location'], '/lists/the-only-list-in-the-world/')
