from selenium import webdriver
from .server_tools import reset_database
from selenium.webdriver.common.keys import Keys
# from django.test import LiveServerTestCase
from django.conf import settings
from selenium.common.exceptions import WebDriverException
from django.contrib.staticfiles.testing import StaticLiveServerTestCase
# from unittest import skip
from .server_tools import create_session_on_server
from .management.commands.create_session import create_pre_authenticated_session
from datetime import datetime
import time
import os

MAX_WAIT = 20
SCREEN_DUMP_LOCATION = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'screendumps'
)


class FunctionalTest(StaticLiveServerTestCase):
	def setUp(self):

		self.browser = webdriver.Firefox()
		self.staging_server = os.environ.get('STAGING_SERVER')
		if self.staging_server:
			self.live_server_url = 'http://' + self.staging_server + '/'
			reset_database(self.staging_server)

	def tearDown(self):
		if self._test_has_failed():
			if not os.path.exists(SCREEN_DUMP_LOCATION):
				os.makedirs(SCREEN_DUMP_LOCATION)
			for ix, handle in enumerate(self.browser.window_handles):
				self._windowid = ix
				self.browser.switch_to_window(handle)
				self.take_screenshot()
				self.dump_html()
		self.browser.quit()
		super().tearDown()

	def create_pre_authenticated_session(self, email, password):
		if self.staging_server:
			pass
		    # session_key = create_session_on_server(self.staging_server, email, password)
		else:
		    session_key = create_pre_authenticated_session(email, password)
		## to set a cookie we need to first visit the domain.
		## 404 pages load the quickest!
		self.browser.get(self.live_server_url + "/404_no_such_url/")
		# We then add a cookie to the browser that matches the session on the
		# server—​on our next visit to the site, the server should recognise
		# us as a logged-in user.
		self.browser.add_cookie(dict(
		    name=settings.SESSION_COOKIE_NAME,
		    value=session_key,
		    secure=False,
		    path='/',
		))
		self.browser.refresh()

	def _test_has_failed(self):
		# slightly obscure but couldn't find a better way!
		return any(error for (method, error) in self._outcome.errors)

	def take_screenshot(self):
		filename = self._get_filename() + '.png'
		print('screenshotting to', filename)
		self.browser.get_screenshot_as_file(filename)

	def dump_html(self):
		filename = self._get_filename() + '.html'
		print('dumping page HTML to', filename)
		with open(filename, 'w') as f:
			f.write(self.browser.page_source)

	def _get_filename(self):
		timestamp = datetime.now().isoformat().replace(':', '.')[:19]
		return '{folder}/{classname}.{method}-window{windowid}-{timestamp}'.format(
			folder=SCREEN_DUMP_LOCATION,
			classname=self.__class__.__name__,
			method=self._testMethodName,
			windowid=self._windowid,
			timestamp=timestamp
		)

	# def add_list_item(self, item_text):
	# 	num_rows = len(self.browser.find_elements_by_css_selector('#id_list_table tr'))
	# 	self.get_item_input_box().send_keys(item_text)
	# 	self.get_item_input_box().send_keys(Keys.ENTER)
	# 	item_number = num_rows + 1
	# 	self.wait_for_row_in_list_table(f'{item_number}: {item_text}')

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
		self.browser.find_element_by_name('Log in')
		navbar = self.browser.find_element_by_css_selector('.navbar')
		self.assertNotIn(email, navbar.text)
