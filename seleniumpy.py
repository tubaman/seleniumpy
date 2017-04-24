import selenium.webdriver


class WebDriverLookup(object):

    def __getattr__(self, name):
        obj = getattr(selenium.webdriver, name)
        if issubclass(obj, selenium.webdriver.remote.webdriver.WebDriver):
            return type('WebDriver', (WebDriver,), {'DRIVER_CLASS': obj})
        return obj

webdriver = WebDriverLookup()


class WebDriver(object):

    def __init__(self, *args, **kwargs):
        self.old_driver = self.DRIVER_CLASS(*args, **kwargs)

    def go(self, url):
        return self.old_driver.get(url)

    def find(self, id=None, name=None, xpath=None, link_text=None,
             partial_link_text=None, tag_name=None, class_name=None,
             css_selector=None):
        if id:
            old_element = self.old_driver.find_element_by_id(id)
        elif name:
            old_element = self.old_driver.find_element_by_name(name)
        elif xpath:
            old_element = self.old_driver.find_element_by_xpath(xpath)
        elif link_text:
            old_element = self.old_driver.find_element_by_link_text(link_text)
        elif partial_link_text:
            old_element = self.old_driver.find_element_by_partial_link_text(partial_link_text)
        elif tag_name:
            old_element = self.old_driver.find_element_by_tag_name(tag_name)
        elif class_name:
            old_element = self.old_driver.find_element_by_class_name(class_name)
        elif css_selector:
            old_element = self.old_driver.find_element_by_css_selector(css_selector)
        else:
            raise ValueError("unknown find type")
        return WebElement(old_element)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.old_driver.quit()


class WebElement(object):

    def __init__(self, element):
        self.old_element = element

    def __getattr__(self, name):
        return getattr(self.old_element, name)

    def find(self, id=None, name=None, xpath=None, link_text=None,
             partial_link_text=None, tag_name=None, class_name=None,
             css_selector=None):
        if id:
            old_element = self.old_element.find_element_by_id(id)
        elif name:
            old_element = self.old_element.find_element_by_name(name)
        elif xpath:
            old_element = self.old_element.find_element_by_xpath(xpath)
        elif link_text:
            old_element = self.old_element.find_element_by_link_text(link_text)
        elif partial_link_text:
            old_element = self.old_element.find_element_by_partial_link_text(partial_link_text)
        elif tag_name:
            old_element = self.old_element.find_element_by_tag_name(tag_name)
        elif class_name:
            old_element = self.old_element.find_element_by_class_name(class_name)
        elif css_selector:
            old_element = self.old_element.find_element_by_css_selector(css_selector)
        else:
            raise ValueError("unknown find type")
        return WebElement(old_element)
