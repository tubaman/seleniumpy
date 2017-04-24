import unittest

import seleniumpy


class TestDriver(unittest.TestCase):

    def test_firefox(self):
        with seleniumpy.webdriver.Firefox() as driver:
            driver.go("http://example.org")
            h1 = driver.find(tag_name="h1")
            self.assertEqual(h1.text, "Example Domain")


if __name__ == '__main__':
    unittest.main()
