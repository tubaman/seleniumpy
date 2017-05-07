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
        return new_element(old_element)

    def find_all(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_elements = self.old_driver.find_elements(locator, lookup_value)
        return [new_element(e) for e in old_elements]

    def wait_for(self, duration=5, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        wait = selenium.webdriver.support.ui.WebDriverWait(self.old_driver, duration)
        condition = EC.presence_of_element_located((locator, lookup_value))
        return new_element(wait.until(condition))


class WebElement(Finder):

    MULTI_VALUED_ATTRIBUTES = ('class', 'rel', 'rev', 'accept-charset', 'headers', 'accesskey')

    def __init__(self, element):
        self.old_element = element

    def __getattr__(self, name):
        return getattr(self.old_element, name)

    def __getitem__(self, key):
        value = self.old_element.get_attribute(key)
        if value is None:
            raise KeyError("attribute '%s' not found" % key)
        if key in self.MULTI_VALUED_ATTRIBUTES:
            value = value.split(' ')
        return value

    def __str__(self):
        return "<%s>..</%s>" % (self.tag_name, self.tag_name)

    def find(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_element = self.old_element.find_element(locator, lookup_value)
        return new_element(old_element)

    def find_all(self, **kwargs):
        lookup_type, lookup_value = kwargs.items()[0]
        locator = self.LOCATORS[lookup_type]
        old_elements = self.old_element.find_elements(locator, lookup_value)
        return [new_element(e) for e in old_elements]


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
