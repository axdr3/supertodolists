from selenium import webdriver
# from selenium.webdriver.common.keys import Keys
# from django.test import LiveServerTestCase
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from unittest import skip
import time
import os


MAX_WAIT = 10


class FunctionalTest(StaticLiveServerTestCase):
	def setUp(self):

		self.browser = webdriver.Firefox()
		self.staging_server = os.environ.get('STAGING_SERVER')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server

	def tearDown(self):
		self.browser.quit()

	# A decorator is a way of modifying a function; it takes a function as an argument…​
	def wait(fn):
		# Here’s where we create our modified function.
		def modified_fn(*args, **kwargs):
			start_time = time.time()
			# Here’s our familiar loop, which will keep going, catching the usual
			# exceptions, until our timeout expires.
			while True:
				try:
					# we call our function and return immediately if there are no exceptions.
					return fn(*args, **kwargs)
				except (AssertionError, WebDriverException) as e:
					if time.time() - start_time > MAX_WAIT:
						raise e
					time.sleep(0.5)
		# returns another function as the modified (or "decorated") version.
		return modified_fn

	@wait
	def wait_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	# 	The body of our try/except, instead of being the specific code for examining
	# table rows, just becomes a call to the function we passed in. We also return
	# its return value to be able to exit the loop immediately if no exception is raised.
	@wait
	def wait_for(self, fn):
		return fn()

	def get_item_input_box(self):
		return self.browser.find_element_by_id('id_text')

	@wait
	def wait_to_be_logged_in(self, email):
		self.browser.find_element_by_link_text('Log out')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertIn(email, navbar.text)

	@wait
	def wait_to_be_logged_out(self, email):
		self.browser.find_element_by_name('email')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)
