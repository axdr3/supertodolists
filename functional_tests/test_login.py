from django.core import mail
from selenium.webdriver.common.keys import Keys
import time
import os
import poplib

from .base import FunctionalTest

SUBJECT = 'Your confirmation link for Supertodolists'


class LoginTest(FunctionalTest):
	def test_can_signup_and_then_login(self):

		test_password = 'meudeusdoc3u'
		if self.staging_server:
			test_email = 'axdr3test@gmail.com'
		else:
			test_email = 'edith@example.com'
		# Edith opens supertodolists page
		# Notices a Signup button
		# Clicks on it
		self.browser.get(self.live_server_url)
		self.browser.find_element_by_name('signup-btn').click()
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('password').send_keys(test_password)
		self.browser.find_element_by_name('password2').send_keys(test_password)
		self.browser.find_element_by_name('submit-btn').click()

		# A confirmation email is sent to her email

		# A message appears telling her an email has been sent
		self.wait_for(lambda: self.assertIn(
			"You will be mailed a confirmation link to your email soon.",
			self.browser.find_element_by_tag_name('body').text
		))
		# She is then redirected to the home page
		self.wait_for(lambda: self.assertURLEqual(
			self.live_server_url + '/',
			self.browser.current_url
			)
		)

		# She goes to her email and sees that she receives the confirmation email

		email = self.wait_for_email(test_email, SUBJECT)
		print(email)
		# She notices a Log in button
		# Clicks on it

		self.browser.find_element_by_name('login-btn').click()
		self.browser.find_element_by_name('email').send_keys(test_email)
		self.browser.find_element_by_name('password').send_keys(test_password)
		self.browser.find_element_by_name('submit-btn').click()

		self.wait_for(lambda: self.assertIn(
			f"You are now logged in as {test_email}",
			self.browser.find_element_by_tag_name('body').text
		))


	def wait_for_email(self, test_email, subject):
		if not self.staging_server:
			email = mail.outbox[0]
			self.assertIn(test_email, email.to)
			self.assertEqual(email.subject, subject)
			return email.body
		email_id = None
		start = time.time()
		inbox = poplib.POP3_SSL('pop.gmail.com', port=995)
		try:
			inbox.user(test_email)
			# Before running this, export EMAIL_PASSWORD variable
			passw = os.environ.get('EMAIL_PASSWORD')
			inbox.pass_(passw)
			while time.time() - start < 60:
				# get 10 newest messages
				count, _ = inbox.stat()
				for i in reversed(range(max(1, count - 10), count + 1)):
					print('getting msg', i)
					_, lines, __ = inbox.retr(i)
					lines = [l.decode('utf8') for l in lines]
					print(lines)
					if f'Subject: {subject}' in lines:
						email_id = i
						body = '\n'.join(lines)
						return body
					time.sleep(5)
		finally:
			if email_id:
				inbox.dele(email_id)
			inbox.quit()
