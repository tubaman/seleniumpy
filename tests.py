import unittest

import seleniumpy
from selenium.common.exceptions import TimeoutException


class WebDriverTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = seleniumpy.webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()


class TestDriverContextManager(unittest.TestCase):

    def test_context_manager(self):
        with seleniumpy.webdriver.Chrome() as driver:
            driver.go("http://example.org")


class TestDriverFind(WebDriverTestCase):

    def test_find(self):
        self.driver.go("http://example.org")
        h1 = self.driver.find(tag_name="h1")
        self.assertEqual(h1.text, "Example Domain")

    def test_find_all(self):
        self.driver.go("http://example.org")
        paras = self.driver.find_all(tag_name="p")
        self.assertEqual(paras[0].text, u'This domain is established to be used for illustrative examples in documents. You may use this domain in examples without prior coordination or asking for permission.')
        self.assertEqual(paras[1].text, u'More information...')


class TestDriverWaitFor(WebDriverTestCase):

    def test_wait_for(self):
        self.driver.go("http://example.org")
        h1 = self.driver.wait_for(tag_name="h1", duration=10)
        self.assertEqual(h1.text, "Example Domain")

    def test_wait_for_timeout(self):
        self.driver.go("http://example.org")
        with self.assertRaises(TimeoutException):
            self.driver.wait_for(tag_name="h2", duration=0.250)


class TestSelect(WebDriverTestCase):

    def test_select(self):
        # select is broken on some version of Firefox
        # http://stackoverflow.com/a/42434977
        self.driver.go("https://developer.mozilla.org/en-US/docs/Web/HTML/Element/select")
        elem = self.driver.wait_for(tag_name="select")
        select = seleniumpy.Select(elem)
        self.assertEqual(select.first_selected_option.get_attribute('value'), 'value2')
        select.select(value='value3')
        self.assertEqual(select.first_selected_option.get_attribute('value'), 'value3')


if __name__ == '__main__':
    unittest.main()
