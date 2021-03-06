from selenium import webdriver
from .base import FunctionalTest
from .list_page import ListPage
from .my_lists_page import MyListsPage
import time


def quit_if_possible(browser):
    try:
        browser.quit()
    except:
        pass


class SharingTest(FunctionalTest):

    def test_can_share_a_list_with_another_user(self):
        # Edith is a logged-in user
        self.create_pre_authenticated_session('edith@example.com', 'alo666')

        edith_browser = self.browser
        self.addCleanup(lambda: quit_if_possible(edith_browser))

        # Edith goes to the home page and starts a list
        self.browser = edith_browser
        self.browser.get(self.live_server_url)
        list_page = ListPage(self).add_list_item('Get help')

        # She notices a "Share this list" option
        share_box = self.browser.find_element_by_css_selector(
            'input[name="sharee"]'
        )
        self.assertEqual(
            share_box.get_attribute('placeholder'),
            'your-friend@example.com'
        )

        # time.sleep(10)
        # Her friend Oniciferous is also hanging out on the lists site
        oni_browser = webdriver.Firefox()
        self.browser = oni_browser
        self.addCleanup(lambda: quit_if_possible(oni_browser))
        self.create_pre_authenticated_session('oniciferous@example.com', 'alo666')
        self.browser.get(self.live_server_url)

        oni_browser = self.browser

        self.browser = edith_browser
        # She shares her list.
        # The page updates to say that it's shared with Oniciferous
        list_page.share_list_with('oniciferous@example.com')
        edith_browser = self.browser

        # Oniciferous now goes to the lists page with his browser
        self.browser = oni_browser
        self.browser.find_element_by_link_text('My lists').click()
        # print(self.live_server_url)
        # MyListsPage(self).go_to_my_lists_page()

        # He sees Edith's list in there!
        self.browser.find_element_by_link_text('Get help').click()

        # On the list page, Oniciferous can see says that it's Edith's list
        self.wait_for(lambda: self.assertIn(
            'edith@example.com',
            list_page.get_list_owner()
        ))

        # He adds an item to the list
        list_page.add_list_item('Hi Edith!')

        # When Edith refreshes the page, she sees Oniciferous's addition
        self.browser = edith_browser
        self.browser.refresh()
        list_page.wait_for_row_in_list_table('Hi Edith!', 2)
