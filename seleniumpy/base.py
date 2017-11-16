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
        'tag': selenium.webdriver.common.by.By.TAG_NAME,
        'class_name': selenium.webdriver.common.by.By.CLASS_NAME,
        'cls': selenium.webdriver.common.by.By.CLASS_NAME,
        'klass': selenium.webdriver.common.by.By.CLASS_NAME,
        'css_selector': selenium.webdriver.common.by.By.CSS_SELECTOR,
        'css': selenium.webdriver.common.by.By.CSS_SELECTOR,
    }

    def find(self, **kwargs):
        lookup_type, lookup_value = list(kwargs.items())[0]
        locator = self.LOCATORS[lookup_type]
        old_element = self.find_element(locator, lookup_value)
        return new_element(old_element)

    def find_all(self, **kwargs):
        lookup_type, lookup_value = list(kwargs.items())[0]
        locator = self.LOCATORS[lookup_type]
        old_elements = self.find_elements(locator, lookup_value)
        return [new_element(e) for e in old_elements]

    def find_element(self, locator, lookup_value):
        raise NotImplementedError()

    def find_elements(self, locator, lookup_value):
        raise NotImplementedError()

    def wait_for(self, duration=5, visible=False, **kwargs):
        lookup_type, lookup_value = list(kwargs.items())[0]
        locator = self.LOCATORS[lookup_type]
        wait = self.wait(duration)
        if visible:
            ec = EC.visibility_of_element_located
        else:
            ec = EC.presence_of_element_located
        condition = ec((locator, lookup_value))
        return new_element(wait.until(condition))

    def wait(self, duration):
        raise NotImplementedError()


class WebDriverLookup(object):

    def __getattr__(self, name):
        obj = getattr(selenium.webdriver, name)
        if hasattr(obj, 'current_url'):
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

    def go(self, url):
        self.old_driver.get(url)

    def quit(self):
        return self.old_driver.quit()

    def find_element(self, locator, lookup_value):
        return self.old_driver.find_element(locator, lookup_value)

    def find_elements(self, locator, lookup_value):
        return self.old_driver.find_elements(locator, lookup_value)

    def wait(self, duration):
        return selenium.webdriver.support.ui.WebDriverWait(self.old_driver,
                                                           duration)
    @property
    def page_source(self):
        return self.old_driver.page_source

    def get_cookies(self):
        return self.old_driver.get_cookies()

    def add_cookie(self, cookie):
        return self.old_driver.add_cookie(cookie)


class WebElement(Finder):

    MULTI_VALUED_ATTRIBUTES = ('class', 'rel', 'rev', 'accept-charset',
                               'headers', 'accesskey')

    def __init__(self, element):
        self.old_element = element

    def __getitem__(self, key):
        value = self.old_element.get_attribute(key)
        if value is None:
            raise KeyError("attribute '%s' not found" % key)
        if key in self.MULTI_VALUED_ATTRIBUTES:
            value = value.split(' ')
        return value

    def __str__(self):
        return "<%s>..</%s>" % (self.tag_name, self.tag_name)

    @property
    def text(self):
        return self.old_element.text

    @text.setter
    def text(self, text):
        self.old_element.clear()
        self.old_element.send_keys(text)

    def find_element(self, locator, lookup_value):
        return self.old_element.find_element(locator, lookup_value)

    def find_elements(self, locator, lookup_value):
        return self.old_element.find_elements(locator, lookup_value)

    def wait(self, duration):
        return selenium.webdriver.support.ui.WebDriverWait(self.old_element,
                                                           duration)
    def click(self):
        self.old_element.click()

    @property
    def is_displayed(self):
        return self.old_element.is_displayed()


class Select(WebElement):

    def __init__(self, element):
        super(Select, self).__init__(element)
        self.old_select = selenium.webdriver.support.ui.Select(element)

    @property
    def options(self):
        return [new_element(o) for o in self.old_select.options]

    @property
    def selected_options(self):
        return [new_element(o) for o in self.old_select.all_selected_options]

    def select(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        method_name = 'select_by_' + lookup_type
        method = getattr(self.old_select, method_name)
        return method(lookup_value)

    def deselect(self, **kwargs):
        try:
            lookup_type, lookup_value = kwargs.items()[0]
        except IndexError:
            return self.old_select.deselect_all()
        else:
            method_name = 'deselect_by_' + lookup_type
            method = getattr(self.old_select, method_name)
            return method(lookup_value)


def new_element(old_element):
    if old_element.tag_name == 'select':
        return Select(old_element)
    else:
        return WebElement(old_element)
