# from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from .base import FunctionalTest
from lists.tests.test_forms import DUPLICATE_ITEM_ERROR
import time


class ItemValidationTest(FunctionalTest):

	def get_error_element(self):
		return self.browser.find_element_by_css_selector('.show-errors')

	def test_cannot_add_empty_list_items(self):
		# Edith goes to the home page and accidentally tries to submit
		# an empty list item. She hits Enter on the empty input box
		self.browser.get(self.live_server_url)
		self.get_item_input_box().send_keys(Keys.ENTER)

		# The browser intercepts the request, and does not load the
		# list page
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))

		# She starts typing some text for the new item and the error disappears
		self.get_item_input_box().send_keys('Buy milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))

		# And she can submit it successfully
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')

		# Perversely, she now decides to submit a second blank list item
		self.get_item_input_box().send_keys(Keys.ENTER)

		# Again, the browser will not comply
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:invalid'
		))

		# And she can correct it by filling some text in
		self.get_item_input_box().send_keys('Make tea')
		self.wait_for(lambda: self.browser.find_elements_by_css_selector(
			'#id_text:valid'
		))
		self.get_item_input_box().send_keys(Keys.ENTER)
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Make tea')

	def test_cannot_add_duplicate_items(self):

		self.browser.get(self.live_server_url)
		self.add_list_item('Buy milk')

		# Try adding same item

		self.get_item_input_box().send_keys('Buy milk')
		self.get_item_input_box().send_keys(Keys.ENTER)

		time.sleep(0.5)

		self.wait_for(lambda: self.assertEqual(
			self.get_error_element().text,
			DUPLICATE_ITEM_ERROR)
		)

		# Add different item

		# self.get_item_input_box().clear()
		self.get_item_input_box().send_keys('Buy dope')
		self.get_item_input_box().send_keys(Keys.ENTER)
		# Verify it hasn't accepted same item
		self.wait_for_row_in_list_table('1: Buy milk')
		self.wait_for_row_in_list_table('2: Buy dope')

	def test_error_messages_are_cleared_on_input(self):
		# Edith starts a list and causes a validation error:
		self.browser.get(self.live_server_url)
		self.add_list_item('Banter too thick')

		self.get_item_input_box().send_keys('Banter too thick')
		self.get_item_input_box().send_keys(Keys.ENTER)

		# is_displayed() tells you whether an element is visible or not.
		self.wait_for(lambda: self.assertTrue(
			self.get_error_element().is_displayed()
		))

		# She starts typing in the input box to clear the error
		self.get_item_input_box().send_keys('a')

		# She is pleased to see that the error message disappears
		self.wait_for(lambda: self.assertFalse(
			self.get_error_element().is_displayed()
		))
