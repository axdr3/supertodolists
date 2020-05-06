from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest


class NewVisitorTest(unittest.TestCase):
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)

	def tearDown(self):
		self.browser.quit()

	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		self.browser.get('http://localhost:8000')

		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# She is invited to enter a to-do list straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
			inputbox.get_attribute('placeholder'),
			'Enter a to-do item'
		)

		# She types'Buy peacock feathers' into a text-box
		inputbox.send_keys('Buy peacock feathers')

		# When she hits enter , the page updates, and now the page lists
		# "1: Buy peacock feathers" as an item in a todo list
		inputbox.send_keys(Keys.ENTER)

		import time
		time.sleep(5)

		self.check_for_row_in_list_table('1: Buy peacock feathers')
		self.check_for_row_in_list_table('2: Use peacock feathers to make a fly')

		# There is still a text box inviting her to add another item. She
		# enters "Use peacock feathers to make a fly"
		self.fail('Finish!x')
		# The page updates again, shows both items

		# Edith wonders if the site will remember her list. Then she sees
		# that the site has generated a unique URL for her -- there is some
		# explanatory text to that effect

		# She visits that URL -- her todo list still there

		# Satisfied she goes back to sleep


if __name__ == '__main__':
	unittest.main(warnings='ignore')
