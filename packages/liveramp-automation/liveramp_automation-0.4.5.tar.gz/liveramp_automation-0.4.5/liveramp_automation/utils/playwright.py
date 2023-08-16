import os
from urllib.parse import urlparse, urlunsplit

from liveramp_automation.helpers.file import FileHelper
from liveramp_automation.utils.allure import allure_attach_text
from liveramp_automation.utils.log import Logger
from liveramp_automation.utils.time import MACROS


class PlaywrightUtils:
    """
    Utility class for Playwright operations.

    This class provides methods for navigating URLs and capturing screenshots using Playwright.

    :param page: Playwright page object.
    :type page: Playwright Page
    """

    def __int__(self, page):
        """
        Initialize PlaywrightUtils with a page object.

        :param page: Playwright page object.
        """
        self.page = page

    def navigate_url(self, scheme=None, host_name=None, path=None, query=None):
        """
        Navigate to a URL with optional components.

        :param scheme: URL scheme (e.g., 'http', 'https').
        :param host_name: Host name or IP address.
        :param path: URL path.
        :param query: URL query string.
        :return: None
        """
        parsed_uri = urlparse(self.page.url)
        url = urlunsplit((parsed_uri.scheme if scheme is None else scheme,
                          parsed_uri.hostname if host_name is None else host_name,
                          parsed_uri.path if path is None else path,
                          parsed_uri.query if query is None else query,
                          ''))
        Logger.info("Navigating to: {}".format(url))
        allure_attach_text("Navigating to:", url)
        try:
            self.page.goto(url)
        except Exception as error:
            Logger.error("An error occurred while navigating: {}".format(error))

    def savescreenshot(self, screenshot_name):
        """
        Save a screenshot of the current page.

        :param screenshot_name: Name for the saved screenshot.
        :return: None
        """
        data_dict = FileHelper.read_init_file("/", "pytest.ini", "r")
        file_path = data_dict.get('screenshot', "reports/")
        my_screenshot_name = "{}_{}.png".format(MACROS["now"], screenshot_name)
        full_path = os.path.join(file_path, my_screenshot_name)
        Logger.info("Saving screenshot: {}".format(full_path))
        allure_attach_text("Saving screenshot to:", full_path)
        try:
            self.page.screenshot(path=full_path)
        except Exception as error:
            Logger.error("An error occurred while saving screenshot: {}".format(error))
