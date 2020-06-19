from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage
from django.conf import settings
import time


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass

class MultipleBrowsersTest(FunctionalTest):

	# def test_browsers(self):


	# 	self.create_pre_authenticated_session('edith@example.com')
	# 	self.browser.get(self.live_server_url)

	# 	self.browser.quit()
	# 	# time.sleep(100)
	# 	self.setUp()
	# 	self.create_pre_authenticated_session('oniciferous@example.com')
	# 	self.browser.get(self.live_server_url)
	# 	time.sleep(10)

	def test_browsers2(self):

		self.create_pre_authenticated_session('edith@example.com')
		self.browser.get(self.live_server_url)
		edith_browser = self.browser

		time.sleep(10)
		oni_browser = webdriver.Firefox()
		self.browser = oni_browser
		self.create_pre_authenticated_session('oniciferous@example.com')
		self.browser.get(self.live_server_url)

		oni_browser = self.browser
		self.browser = edith_browser
		time.sleep(10)

		list_page = ListPage(self).add_list_item('Get help')
		# self.browser.get(self.live_server_url + '/users/' + 'edith@example.com')
		share_box = self.browser.find_element_by_css_selector(
			'input[name="sharee"]'
		)
		self.assertEqual(
			share_box.get_attribute('placeholder'),
			'your-friend@example.com'
		)

		# self.browser.find_element_by_link_text('My lists').click()
		list_page.share_list_with('oniciferous@example.com')

		edith_browser = self.browser
		time.sleep(10)
		# edith_browser.quit()
		# self.browser = oni_browser
		edith_browser.quit()
		oni_browser.quit()
