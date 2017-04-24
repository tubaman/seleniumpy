import selenium.webdriver
from selenium.webdriver.support import expected_conditions as EC


class Finder(object):

    LOCATORS = {
        'id': selenium.webdriver.common.by.By.ID,
        'xpath': selenium.webdriver.common.by.By.XPATH,
        'link_text': selenium.webdriver.common.by.By.LINK_TEXT,
        'partial_link_text': selenium.webdriver.common.by.By.PARTIAL_LINK_TEXT,
        'name': selenium.webdriver.common.by.By.NAME,
        'tag_name': selenium.webdriver.common.by.By.TAG_NAME,
        'class_name': selenium.webdriver.common.by.By.CLASS_NAME,
        'css_selector': selenium.webdriver.common.by.By.CSS_SELECTOR,
    }


class WebDriverLookup(object):

    def __getattr__(self, name):
        obj = getattr(selenium.webdriver, name)
        if issubclass(obj, selenium.webdriver.remote.webdriver.WebDriver):
            return type('WebDriver', (WebDriver,), {'DRIVER_CLASS': obj})
        return obj

webdriver = WebDriverLookup()


class WebDriver(Finder):

    def __init__(self, *args, **kwargs):
        self.old_driver = self.DRIVER_CLASS(*args, **kwargs)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.old_driver.quit()

    def __getattr__(self, name):
        return getattr(self.old_driver, name)

    def go(self, url):
        self.old_driver.get(url)

    def find(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_element = self.old_driver.find_element(locator, lookup_value)
        return WebElement(old_element)

    def find_all(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_elements = self.old_driver.find_elements(locator, lookup_value)
        return [WebElement(e) for e in old_elements]

    def wait_for(self, duration=5, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        wait = selenium.webdriver.support.ui.WebDriverWait(self.old_driver, duration)
        condition = EC.presence_of_element_located((locator, lookup_value))
        return WebElement(wait.until(condition))


class WebElement(Finder):

    def __init__(self, element):
        self.old_element = element

    def __getattr__(self, name):
        return getattr(self.old_element, name)

    def find(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_element = self.old_element.find_element(locator, lookup_value)
        return WebElement(old_element)

    def find_all(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_elements = self.old_element.find_elements(locator, lookup_value)
        return [WebElement(e) for e in old_elements]
