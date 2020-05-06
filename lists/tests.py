from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
import re
from .views import home_page

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

	def test_home_page_can_save_a_POST_request(self):
		request = HttpRequest()
		request.method = 'POST'
		request.POST['item_text'] = 'A new list item'

		response = home_page(request)

		self.assertIn('A new list item', response.content.decode())

		expected_html = render_to_string(
			'lists/home.html',
			{'new_item_text': 'A new list item'},
			request=request,
		)
		
		self.assertEqual(
			remove_csrf(response.content.decode()),
			remove_csrf(expected_html)
		)
