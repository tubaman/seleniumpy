import unittest

import seleniumpy
from selenium.common.exceptions import TimeoutException


class WebDriverTestCase(unittest.TestCase):

    def setUp(self):
        self.driver = seleniumpy.webdriver.Firefox()

    def tearDown(self):
        self.driver.quit()


class TestDriverContextManager(unittest.TestCase):

    def test_context_manager(self):
        with seleniumpy.webdriver.Firefox() as driver:
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
        self.driver.go("https://www.w3schools.com/tags/tryit.asp?filename=tryhtml_select")
        self.driver.switch_to.frame("iframeResult")
        elem = self.driver.wait_for(tag_name="select")
        select = seleniumpy.Select(elem)
        select.select(value='audi')
        self.assertEqual(select.first_selected_option.get_attribute('value'), 'audi')


if __name__ == '__main__':
    unittest.main()
