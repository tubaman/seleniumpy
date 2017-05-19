import unittest
import mock

import selenium

import seleniumpy


class TestDriverLookup(unittest.TestCase):

    def test_driver_lookup(self):
        obj = seleniumpy.webdriver.Chrome
        self.assertEquals(obj.DRIVER_CLASS, selenium.webdriver.Chrome)

    def test_non_driver_lookup(self):
        obj = seleniumpy.webdriver.support.ui.WebDriverWait
        self.assertEquals(obj, selenium.webdriver.support.ui.WebDriverWait)


class WebDriverTestCase(unittest.TestCase):

    def setUp(self):
        self.patcher = mock.patch('seleniumpy.selenium.webdriver.Chrome')
        self.mock_webdriver = self.patcher.start()
        self.driver = seleniumpy.webdriver.Chrome()

    def tearDown(self):
        self.driver.quit()
        self.patcher.stop()


class TestDriverContextManager(unittest.TestCase):

    @mock.patch('seleniumpy.selenium.webdriver')
    def test_context_manager(self, mock_webdriver):
        driver = seleniumpy.webdriver.Chrome()
        driver.__exit__(None, None, None)
        driver.old_driver.quit.assert_called()


class TestDriverFind(WebDriverTestCase):

    def test_find(self):
        self.driver.go("http://example.org")
        h1 = self.driver.find(tag_name="h1")
        self.driver.old_driver.find_element.assert_called_with(
            selenium.webdriver.common.by.By.TAG_NAME, 'h1')

    def test_find_all(self):
        self.driver.go("http://example.org")
        paras = self.driver.find_all(tag_name="p")
        self.driver.old_driver.find_elements.assert_called_with(
            selenium.webdriver.common.by.By.TAG_NAME, 'p')


class TestDriverWaitFor(WebDriverTestCase):

    @mock.patch('seleniumpy.EC.presence_of_element_located')
    @mock.patch('seleniumpy.selenium.webdriver.support.ui.WebDriverWait')
    def test_wait_for(self, mock_wait_cls, mock_ec):
        self.driver.go("http://example.org")
        h1 = self.driver.wait_for(tag_name="h1", duration=10)
        mock_wait_cls.assert_called_with(self.driver.old_driver, 10)
        mock_ec.assert_called_with((selenium.webdriver.common.by.By.TAG_NAME, 'h1'))
        mock_wait = mock_wait_cls.return_value
        mock_wait.until.assert_called_with(mock_ec.return_value)


if __name__ == '__main__':
    unittest.main()
