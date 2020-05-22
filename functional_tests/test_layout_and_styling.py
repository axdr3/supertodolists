from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from django.test import LiveServerTestCase
from unittest import skip
from .base import FunctionalTest
import time


MAX_WAIT = 10



class LayoutAndStylingTest(FunctionalTest):

	def test_layout_and_styling(self):
		# Edith goes to the home page
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)

		# She notices the input box is nicely centered
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=5
		)

		# She starts a new list and sees the input is nicely
		# centered there too
		inputbox.send_keys('testing\n')
		inputbox = self.get_item_input_box()
		self.assertAlmostEqual(
			inputbox.location['x'] + inputbox.size['width'] / 2,
			512,
			delta=5
		)
