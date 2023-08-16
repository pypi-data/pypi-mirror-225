import os
from urllib.parse import urlparse, urlunsplit
from liveramp_automation.helpers.file import FileHelper
from liveramp_automation.utils.log import Logger
from liveramp_automation.utils.time import MACROS, fixed_wait
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, JavascriptException, NoSuchElementException


class SeleniumUtils:

    def __init__(self, driver):
        self.driver = driver

    def navigate_url(self, scheme=None, host_name=None, path=None, query=None):
        """
        Navigate to the provided URL.

        :param scheme: The protocol to use for the connection, such as 'https' or 'http'.
        :param host_name: The domain name of the web server, e.g., 'www.liveramp.com'.
        :param path: The specific route or location on the web server, e.g., '/query/vi/save'.
        :param query: Additional parameters to customize the request.
        :return: None
        """
        parsed_uri = urlparse(self.driver.current_url)
        self.driver.get(urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                                    parsed_uri.netloc if host_name is None else host_name,
                                    parsed_uri.path if path is None else path,
                                    parsed_uri.query if query is None else query,
                                    '')))

    def save_screenshot(self, screenshot_name):
        """ Save a screenshot to the specified destination.
        If pytest.ini file has not set up the default directory for screenshot,
        it will use the reports directory instead.
        :param screenshot_name: The desired name for the screenshot file.
        :return: None
        """
        config_data = FileHelper.read_init_file("", "pytest.ini", "r")
        Logger.info(config_data)
        Logger.debug(type(config_data))
        screenshot_dir = config_data.get('screenshot', 'reports')
        Logger.info(screenshot_dir)
        Logger.info(type(screenshot_dir))
        screenshot_filename = "{}_{}.png".format(MACROS["now"], screenshot_name)
        screenshot_path = os.path.join(screenshot_dir + screenshot_filename)
        self.driver.save_screenshot(screenshot_path)

    def get_url(self, url):
        """ Open the page using the provided URL.

        :param url:The URL of the page to be opened.
        :return:None
        """
        self.driver.get(url)

    def refresh_page(self):
        """ Refresh the page.

        :return:
        """
        self.driver.refresh()
        Logger.debug("Page Refreshed With URL {}".format(self.driver.current_url))

    def find_element_by_dict(self, dictionary, timeout_second=5):
        """ Retrieve the first element that matches the criteria specified in the dictionary.

        :param dictionary: A dictionary containing criteria for element identification.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 5 seconds).
        :return: The found element or None if not found.
        """
        by_type = (next(iter(dictionary)))
        locator = dictionary.get(by_type)
        try:
            return WebDriverWait(self.driver, timeout_second).until(EC.presence_of_element_located((by_type, locator)))
        except TimeoutException:
            Logger.info("element {} was not found".format(locator))
            return None

    def find_elements_by_dict(self, dictionary, timeout_second=3):
        """ Search for all elements that match the criteria specified in the dictionary.

        :param dictionary: A dictionary containing criteria for element identification.
        :param timeout_second: The maximum time, in seconds, to wait for elements to appear (default is 3 seconds).
        :return: A list of found elements, which can be empty if no elements are found.
        """
        by_type = (next(iter(dictionary)))
        locator = dictionary.get(by_type)
        try:
            return WebDriverWait(self.driver, timeout_second).until(
                EC.presence_of_all_elements_located((by_type, locator)))
        except TimeoutException:
            Logger.info("element {} was not found".format(locator))

    def find_element(self, by_type, locator, timeout_second=3):
        """ Locate the first element and wait for it to load within the specified maximum timeout_second time.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: The found element or None if not found.
        """
        try:
            return WebDriverWait(self.driver, timeout_second).until(EC.presence_of_element_located((by_type, locator)))
        except TimeoutException:
            Logger.info("element {} was not found".format(locator))
            return None

    def find_element_by_css(self, locator, timeout_second=3, by_type=By.CSS_SELECTOR):
        """ Search for the first element using the CSS_SELECTOR with the implementation of Explicit Waits.

        :param locator: The CSS selector used to locate the element.
        :param by_type: The method used for locating the element (default is CSS_SELECTOR).
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: The found element or None if not found.
        """
        return self.find_element(by_type, locator, timeout_second)

    def find_element_by_tag(self, locator, timeout_second=3, by_type=By.TAG_NAME):
        """ Search for the first element using the TAG_NAME with the implementation of Explicit Waits.

        :param locator: The CSS selector used to locate the element.
        :param by_type: The method used for locating the element.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: The found element or None if not found.
        """
        return self.find_element(by_type, locator, timeout_second)

    def find_element_by_id(self, locator, timeout_second=3, by_type=By.ID):
        """ Search for the first element using the ID with the implementation of Explicit Waits.

        :param locator: The CSS selector used to locate the element.
        :param by_type: The method used for locating the element.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: The found element or None if not found.
        """
        return self.find_element(by_type, locator, timeout_second)

    def find_elements(self, by_type, locator, timeout_second=3):
        """ Find multiple elements using the specified method and locator, and wait for them
        to load within the specified maximum timeout_second time.

        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 3 seconds).
        :return: A list of found elements, which can be empty if no elements are found.
        """
        try:
            return WebDriverWait(self.driver, timeout_second).until(
                EC.presence_of_all_elements_located((by_type, locator)))
        except TimeoutException:
            Logger.info("element {} was not found".format(locator))

    def find_elements_by_css(self, locator, timeout_second=3, by_type=By.CSS_SELECTOR):
        """ Search for multiple elements using the CSS_SELECTOR method and implement Explicit Waits.

        :param locator: The CSS selector used to locate the elements.
        :param by_type: The method used for locating the elements (default is CSS_SELECTOR).
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 3 seconds).
        :return: A list of found elements, which can be empty if no elements are found.
        """
        return self.find_elements(by_type, locator, timeout_second)

    def count_elements(self, by_type, locator, timeout_second=5):
        """ Obtain the count of matching elements within the specified maximum timeout_second duration.

        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 5 seconds).
        :return: The count of matching elements or 0 if none are found.
        """
        try:
            return len(
                WebDriverWait(self.driver, timeout_second).until(
                    EC.visibility_of_all_elements_located((by_type, locator))))
        except TimeoutException:
            TimeoutException('element was not found: {}'.format(locator))
        return 0

    def is_element_clickable(self, by_type, locator, timeout_second=3):
        """ Retrieve the clickable status of the element within the specified maximum timeout_second period.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the element to become clickable (default is 3 seconds).
        :return: True if the element is clickable, False if not or if the element is not found.
        """
        WebDriverWait(self.driver, timeout_second).until(EC.element_to_be_clickable((by_type, locator)))

    def is_element_enabled(self, by_type, locator, timeout_second=3):
        """ Return the enabled status of the element within the specified maximum timeout_second time.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: True if the element is enabled, False if not or if the element is not found.
        """
        try:
            return WebDriverWait(self.driver, timeout_second).until(
                EC.presence_of_element_located((by_type, locator))).is_enabled()
        except TimeoutException:
            raise Exception("element {} was not found".format(locator))

    def get_index_elements(self, by_type, locator, timeout_second):
        """ Retrieve the index and a list of elements based on the provided locator.

        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear.
        :return: A list of tuples [(index, element), ...] or an empty list if no elements are found.
        """
        elements = WebDriverWait(self.driver, timeout_second).until(
            EC.visibility_of_all_elements_located((by_type, locator)))
        if elements:
            return [(index, element) for index, element in enumerate(elements)]
        else:
            return []

    def get_text_index_elements(self, text, by_type, locator, timeout_second=3):
        """
       Obtain a list of index_element pairs based on the provided text that matches the text of the locator.

       :param text: The text to match within the element.
       :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
       :param locator: The value of the locator, such as an ID, name, or XPath expression.
       :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 3 seconds).
       :return: e.g. [(0, ele1), (1, ele2)] A list of index-element pairs [(index, element), ...] that contain the specified text.
       """
        index_elements = self.get_index_elements(by_type, locator, timeout_second)
        if index_elements:
            return [index_element for index_element in index_elements if text in index_element[1].text]
        else:
            Logger.info("No elements were found that match the provided text in the locator.")
            return []

    def is_text_found(self, text, by_type, locator, timeout_second=5):
        """ Return a boolean value based on the presence of the identified text.

        :param text: The text to search for within the elements.
        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 5 seconds).
        :return: True if the specified text is found in the identified elements, False otherwise.
        """
        return bool(self.get_text_index_elements(text, by_type, locator, timeout_second))

    def click(self, by_type, locator, delay_second=2, timeout_second=5):
        """ Perform a click action on an element, scrolling if needed for visibility.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param delay_second: The delay_second time, in seconds, before performing the click (default is 2 seconds).
        :param timeout_second: The maximum time, in seconds, to wait for the element to be clickable (default is 5 seconds).
        :return: None
        """
        try:
            WebDriverWait(self.driver, timeout_second).until(EC.element_to_be_clickable((by_type, locator)))
        except TimeoutException:
            Logger.info('Element was not clickable: {}'.format(locator))

        el = self.find_element(by_type, locator)

        try:
            self.driver.execute_script("arguments[0].scrollIntoView();", el)
            el.click()
            return
        except JavascriptException:
            fixed_wait(delay_second)
            Logger.info("Couldn't execute JavaScript: scrollIntoView() for element: {} locator: {}".format(el, locator))

        el = self.find_element(by_type, locator)
        el.click()
        Logger.info("Element found and clicked.")

    def click_no_scroll(self, locator, by_type=By.CSS_SELECTOR):
        """
        Click the element using its CSS selector without scrolling.

        :param locator: The CSS selector of the element.
        :param by_type: The method used for locating the element (default is CSS_SELECTOR).
        :return: None
        """
        el = self.find_element(by_type, locator)
        el.click()

    def click_text(self, text, by_type, locator, timeout_second=3, index=0):
        """
        Retrieve a list of index-element pairs based on the provided text that matches the text of the locator,
        then click the element corresponding to the provided index.

        :param text: The text to search for within the elements.
        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 3 seconds).
        :param index: The index of the element to click (default is 0, the first element).
        :return: None
        """
        index_elements = self.get_text_index_elements(text, by_type, locator, timeout_second)
        if index_elements:
            element_to_click = index_elements[index][1]
            element_to_click.click()

    def hover_over_element_and_click(self, element, by_type=None, locator=None, index=0):
        """
        Hover over the element at index+1 and then click it.

        :param element: The element to hover over and click.
        :param by_type: The method used for locating additional elements, e.g., 'id', 'name', 'xpath', etc. (optional).
        :param locator: The value of the locator for additional elements (optional).
        :param index: The index of the additional element to click (default is 0).
        :return: None
        """
        actions = ActionChains(self.driver)
        actions.move_to_element(element)

        if by_type and locator:
            actions.perform()
            additional_elements = self.find_elements(by_type, locator)
            if index < len(additional_elements):
                additional_elements[index].click()
        else:
            actions.click(element).perform()

    def hover_over_text_and_click(self, text, by_type, locator, click_type=None, click_locator=None, index=0,
                                  timeout_second=7):
        """
        Retrieve a list of index_element pairs based on the provided text that matches the text of the locator.
        Then, hover over and click the element at index+1.

        :param text: The text to search for within the elements.
        :param by_type: The method used for locating the elements, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator, such as an ID, name, or XPath expression.
        :param click_type: The method used for locating the element to click, if different from the hover element (optional).
        :param click_locator: The value of the locator for the element to click (optional).
        :param index: The index of the element to click (default is 0).
        :param timeout_second: The maximum time, in seconds, to wait for the elements to appear (default is 7 seconds).
        :return: None
        """
        index_elements = self.get_text_index_elements(text, by_type, locator, timeout_second)

        if index_elements:
            index_element = index_elements[index] if index < len(index_elements) else index_elements[0]
            self.hover_element_and_click(index_element[1], click_type, click_locator)
        else:
            raise NoSuchElementException('Locator not found: {}'.format(locator))

    def drag_and_drop(self, source_element, target_element):
        """
        Perform a drag-and-drop action from the source element to the target element.

        :param source_element: The element to drag from.
        :param target_element: The element to drop onto.
        :return: None
        """
        ActionChains(self.driver).drag_and_drop(source_element, target_element).perform()

    def click_by_dict(self, dictionary):
        """
        Click the element using a dictionary of provided types.

        :param dictionary: A dictionary containing the locator type as the key and the locator value as the value.
        :return: None
        """
        by_type = next(iter(dictionary))
        locator = dictionary.get(by_type)
        self.click(by_type, locator)

    def click_by_css(self, locator, by_type=By.CSS_SELECTOR):
        """
        Click the element using its CSS selector.

        :param locator: The CSS selector of the element.
        :param by_type: The method used for locating the element (default is CSS_SELECTOR).
        :return: None
        """
        self.click(by_type, locator)

    def type_without_click(self, text, by_type, locator):
        """
        Type text into an input field identified by its locator without performing a click action.

        :param text: The text to type into the input field.
        :param by_type: The method used for locating the input field, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the input field.
        :return: None
        """
        el = self.find_element(by_type, locator)
        el.send_keys(text)

    def select(self, option, by_type, locator):
        """
       Select an option from a dropdown element based on its visible text.

       :param option: The visible text of the option to select.
       :param by_type: The method used for locating the dropdown element, e.g., 'id', 'name', 'xpath', etc.
       :param locator: The value of the locator for the dropdown element.
       :return: None
       """
        _select = Select(self.find_element(by_type, locator))
        _select.select_by_visible_text(option)

    def select_by_dict(self, option, dictionary):
        """
        Select an option from a dropdown element based on its visible text
        using a dictionary of provided types.

        :param option: The visible text of the option to select.
        :param dictionary: A dictionary containing the locator type as the key and the locator value as the value.
        :return: None
        """
        by_type = next(iter(dictionary))
        locator = dictionary.get(by_type)
        _select = Select(self.find_element(by_type, locator))
        _select.select_by_visible_text(option)

    def type_text(self, text, by_type, locator):
        """
        Type text into an input field identified by its locator.

        :param text: The text to type into the input field.
        :param by_type: The method used for locating the input field, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the input field.
        :return: None
        """
        el = self.find_element(by_type, locator)
        el.click()
        el.send_keys(text)

    def type_text_dict(self, text, dictionary):
        """
        Type text into an input field using a dictionary of provided types.

        :param text: The text to type into the input field.
        :param dictionary: A dictionary containing the locator type as the key and the locator value as the value.
        :return: None
        """
        by_type = next(iter(dictionary))
        locator = dictionary.get(by_type)
        self.type_without_click(text, by_type, locator)

    def clear_text(self, by_type, locator, timeout_second=3):
        """
        Clear the text from an input field identified by its locator.

        :param by_type: The method used for locating the input field, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the input field.
        :param timeout_second: The maximum time, in seconds, to wait for the element to appear (default is 3 seconds).
        :return: None
        """
        el = self.find_element(by_type, locator, timeout_second)
        el.click()
        el.clear()

    def type_text_press_enter(self, text, by_type, locator):
        """
        Type text into an input field identified by its locator and press the Enter key.

        :param text: The text to type into the input field.
        :param by_type: The method used for locating the input field, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the input field.
        :return: None
        """
        input_field = self.find_element(by_type, locator)
        input_field.send_keys(text)
        input_field.send_keys(Keys.RETURN)

    def clear_input_box_press_enter(self, by_type, locator, delay_second=3):
        """
        Clear the content of an input box identified by its locator and press the Enter key.

        :param by_type: The method used for locating the input box, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the input box.
        :param delay_second: The delay_second time, in seconds, before performing the click (default is 3 seconds).
        :return: None
        """
        ele = self.find_element(by_type, locator)
        ActionChains(self.driver).double_click(ele).perform()
        ele.send_keys(Keys.DELETE)
        ele.send_keys(Keys.ENTER)
        fixed_wait(delay_second)

    def get_text_from_element(self, page_element):
        """
        Get the text content from a given element.

        :param page_element: The element from which to retrieve the text.
        :return: The text content of the element.
        """
        self.driver.execute_script("arguments[0].scrollIntoView();", page_element)
        return page_element.text

    def get_text(self, by_type, locator):
        """
        Get the text content from an element identified by its locator.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the element.
        :return: The text content of the element.
        """
        el = self.find_element(by_type, locator)
        return self.get_text_from_element(el)

    def get_text_from_page(self):
        """
        Get the text content from the entire page.

        :return: The text content of the page.
        """
        return self.get_text(By.TAG_NAME, "body")

    def get_attribute(self, by_type, locator, attribute):
        """
        Get the value of a specified attribute from an element identified by its locator.

        :param by_type: The method used for locating the element, e.g., 'id', 'name', 'xpath', etc.
        :param locator: The value of the locator for the element.
        :param attribute: The name of the attribute whose value is to be retrieved.
        :return: The value of the specified attribute.
        """
        el = self.find_element(by_type, locator)
        return el.get_attribute(attribute)

    def get_child_elements_by_css_selector(self, by_type, parent_locator, child_css):
        """
        Get child elements of a parent element identified by its locator using a CSS selector.

        :param by_type: The method used for locating the parent element, e.g., 'id', 'name', 'xpath', etc.
        :param parent_locator: The value of the locator for the parent element.
        :param child_css: The CSS selector for the child elements.
        :return: A list of child elements matching the CSS selector.
        """
        parent_element = self.find_element(by_type, parent_locator)
        return parent_element.find_elements_by_css_selector(child_css)

    def switch_window(self):
        """
        Switch to a different window handle.

        :return: None
        """
        fixed_wait()
        handles = self.driver.window_handles
        for handle in handles:
            if handle != self.driver.current_window_handle:
                self.driver.switch_to.window(handle)

    def wait_for_title(self, title, timeout_second=20):
        """
        Wait for the browser window's title to contain the specified title text.

        :param title: The title text to wait for.
        :param timeout_second: The maximum time, in seconds, to wait for the title (default is 20 seconds).
        :return: None
        """
        try:
            WebDriverWait(self.driver, timeout_second).until(EC.title_contains(title))
        except TimeoutException:
            pass

    def wait_for_link(self, link_text, timeout_second=20):
        """
        Wait for a link with the specified link text to appear in the page.

        :param link_text: The link text to wait for.
        :param timeout_second: The maximum time, in seconds, to wait for the link (default is 20 seconds).
        :return: None
        """
        try:
            WebDriverWait(self.driver, timeout_second).until(EC.presence_of_element_located((By.LINK_TEXT, link_text)))
        except TimeoutException:
            pass

    def find_button_equal_text_click(self, button_text, css_selector='button'):
        """
        Find and click a button with the specified exact text and CSS selector.

        :param button_text: The exact text of the button to find and click.
        :param css_selector: The CSS selector for locating the buttons.
        :return: None
        """
        action_buttons = self.find_elements(By.CSS_SELECTOR, css_selector)
        for button in action_buttons:
            if button_text == button.text:
                button.click()
                fixed_wait(1)
                break

    def find_button_contain_text_click(self, button_text, css_selector='button'):
        """
        Find and click a button containing the specified text and matching the CSS selector.

        :param button_text: The text to search for in the button's text content.
        :param css_selector: The CSS selector for locating the buttons.
        :return: None
        """
        action_buttons = self.find_elements(By.CSS_SELECTOR, css_selector)
        for button in action_buttons:
            if button_text in button.text:
                button.click()
                fixed_wait(1)
                break

    def select_radio_equal_text_click(self, radio_text, css_selector):
        """
        Select a radio button when its label text is equal to the expected text.

        :param radio_text: The expected label text of the radio button.
        :param css_selector: The CSS selector for locating the radio button labels.
        :return: None
        """
        element_options = self.find_elements(By.CSS_SELECTOR, css_selector)
        for ele in element_options:
            if radio_text == ele.text:
                radio_ele = ele.find_element(By.CSS_SELECTOR, 'input[type="radio"]')
                radio_ele.click()
                fixed_wait()
                break

    def find_row_contain_text_click_button(self, row_text, button_text, row_css, button_css):
        """
        Find a table row containing specified text, locate a button in that row, and click the button.

        :param row_text: The text to search for in the table row.
        :param button_text: The text of the button within the row to click.
        :param row_css: The CSS selector for locating table rows.
        :param button_css: The CSS selector for locating buttons within the rows.
        :return: None
        """
        action_rows = self.find_elements(By.CSS_SELECTOR, row_css)
        for row in action_rows:
            if row_text in row.text:
                action_buttons = row.find_elements(By.CSS_SELECTOR, button_css)
                for button in action_buttons:
                    if button_text in button.text:
                        button.click()
                        fixed_wait()
                        return

    def find_row_contain_text_return_cell_element(self, row_text, row_css, cell_css):
        """
        Find a table row containing specified text, locate a cell in that row, and return the cell element.

        :param row_text: The text to search for in the table row.
        :param row_css: The CSS selector for locating table rows.
        :param cell_css: The CSS selector for locating cells within the rows.
        :return: The WebElement representing the target cell, or None if not found.
        """
        element_rows = self.find_elements(By.CSS_SELECTOR, row_css)
        if element_rows is None:
            return None
        for row in element_rows:
            if row_text in row.text:
                target_cell = row.find_element(By.CSS_SELECTOR, cell_css)
                return target_cell
        return None

    def find_row_contain_text_return_cell_text(self, row_text, row_css, cell_css):
        """
        Find a table row containing specified text, locate a cell in that row, and return the text content of the cell.

        :param row_text: The text to search for in the table row.
        :param row_css: The CSS selector for locating table rows.
        :param cell_css: The CSS selector for locating cells within the rows.
        :return: The text content of the target cell, or None if not found.
        """
        element_rows = self.find_elements(By.CSS_SELECTOR, row_css)
        if element_rows is None:
            return None
        for row in element_rows:
            if row_text in row.text:
                target_cell = row.find_element(By.CSS_SELECTOR, cell_css)
                return target_cell.text
        return None

    def find_row_contain_text_click_element(self, row_text, row_css, element_css, n=1):
        """
        Find a table row containing specified text, locate an element in that row, and click it.

        :param row_text: The text to search for in the table row.
        :param row_css: The CSS selector for locating table rows.
        :param element_css: The CSS selector for locating the elements within the rows.
        :param n: The number of elements to click (default is 1).
        :return: None
        """
        ele_rows = self.find_elements(By.CSS_SELECTOR, row_css)
        flag = 0
        for row in ele_rows:
            if row_text in row.text:
                flag += 1
                action_element = row.find_element(By.CSS_SELECTOR, element_css)
                try:
                    WebDriverWait(self.driver, 30).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_css)))
                except TimeoutException:
                    Logger.info(f"Element {row.text} never became clickable")
                self.driver.execute_script("arguments[0].scrollIntoView();", action_element)
                action_element.click()
                fixed_wait(1)
                if n is not None and n >= flag:
                    return

    def find_row_contain_two_texts_click(self, row_text, another_text, row_css, element_css, n=1):
        """
        Compare values in two columns of a table and click an element if the conditions are met.

        :param row_text: Text to search for in the table row.
        :param another_text: Another text to search for in the table row.
        :param row_css: CSS selector for locating table rows.
        :param element_css: CSS selector for locating the element within the rows to click.
        :param n: Number of elements to click (default is 1).
        :return: Number of elements clicked.
        """
        ele_rows = self.find_elements(By.CSS_SELECTOR, row_css)
        flag = 0
        for row in ele_rows:
            if row_text.lower() in row.text.lower() and another_text.lower() in row.text.lower():
                flag += 1
                action_element = row.find_element(By.CSS_SELECTOR, element_css)
                action_element.click()
                fixed_wait(1)
                if n is not None and n >= flag:
                    return flag
        return flag

    def find_contain_text_hover_click(self, text, css_selector, hover_css_selector):
        """
        Find a row containing the specified text, hover over the specified element, and click it.

        :param text: Text to search for in the table row.
        :param css_selector: CSS selector for locating table rows.
        :param hover_css_selector: CSS selector for locating the element to hover over.
        :return: True if successful, False otherwise.
        """
        rows = self.find_elements(By.CSS_SELECTOR, css_selector)
        for row in rows:
            if text in row.text:
                view_button = row.find_element(By.CSS_SELECTOR, hover_css_selector)
                hover = ActionChains(self.driver).move_to_element(view_button)
                hover.perform()
                view_button.click()
                fixed_wait()  # Adjust the delay_second here if needed
                return True
        return False

    def find_contain_text_hower_click_another(self, text, css_selector, hover_css_selector, click_css_selector):
        """
        Find a row containing the specified text, hover over a specified element, and click another element.

        :param text: Text to search for in the table row.
        :param css_selector: CSS selector for locating table rows.
        :param hover_css_selector: CSS selector for locating the element to hover over.
        :param click_css_selector: CSS selector for locating the element to click after hovering.
        :return: None
        """
        rows = self.find_elements(By.CSS_SELECTOR, css_selector)
        for row in rows:
            if text in row.text:
                view_button = row.find_element(By.CSS_SELECTOR, hover_css_selector)
                hover = ActionChains(self.driver).move_to_element(view_button)
                hover.perform()
                fixed_wait()  # Adjust the delay_second here if needed
                row.find_element(By.CSS_SELECTOR, click_css_selector).click()
                fixed_wait()  # Adjust the delay_second here if needed
                break

    def find_contain_text_type_text(self, search_text, css_selector, type_text_css_selector, text_to_type):
        """
        Find a row containing the specified text, locate an input element, and type text into it.

        :param search_text: Text to search for in the table row.
        :param css_selector: CSS selector for locating table rows.
        :param type_text_css_selector: CSS selector for locating the input element.
        :param text_to_type: Text to type into the input element.
        :return: True if the text is found and typed, False otherwise.
        """
        elems = self.find_elements(By.CSS_SELECTOR, css_selector)
        for elem in elems:
            if search_text in elem.text:
                type_text_elem = elem.find_element(By.CSS_SELECTOR, type_text_css_selector)
                self.driver.execute_script("arguments[0].scrollIntoView();", type_text_elem)
                type_text_elem.click()
                type_text_elem.clear()
                type_text_elem.send_keys(text_to_type)
                fixed_wait()  # Adjust the delay_second here if needed
                return True
        return False

    def click_presentation_contain_role_click(self, ul_role, role_name):
        """
        Click an item within a presentation list based on a specific role name.

        :param ul_role: The role attribute of the <ul> element containing the list.
        :param role_name: The role name to be matched within the list.
        :return: None
        """
        rows = self.find_elements(self.driver, By.CSS_SELECTOR, f'div[role="presentation"] ul[role="{ul_role}"] li')
        for row in rows:
            if role_name in row.text:
                row.click()
                break
        fixed_wait()  # Adjust the delay_second here if needed

    def close_popup_banner(self):
        """
        Close the popup banner using a matched CSS selector pattern.

        :return: None
        """
        dialog_button = self.find_element(self.driver, By.CSS_SELECTOR, 'button[id^="pendo-button"]')
        if dialog_button is None:
            dialog_button = self.find_element(self.driver, By.CSS_SELECTOR, 'button[id^="pendo-close"]')
        if dialog_button is not None:
            dialog_button.click()

    def close_pendo_banners(self):
        """
        Close all popup banners using a matched CSS selector pattern.

        :return: None
        """
        dialog_buttons = self.find_elements(self.driver, By.CSS_SELECTOR, 'button[id^="pendo-close-guide"]')
        for button in dialog_buttons:
            button.click()
            fixed_wait()
