import numpy as np
import datetime as dt

# Selenium imports
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException


class SeleniumBaseScraper:
    def __init__(self, chrome_driver_path: str) -> None:
        self.chrome_driver_path = chrome_driver_path
        self.chrome_options = webdriver.ChromeOptions()
        self.chrome_options.add_argument("--no-sandbox")
        self.chrome_options.add_argument("--disable-gpu")
        self.browser = None

        # List of possible function parameters for financial report frequency.
        self.quarterly_params = [
            "q",
            "Q",
            "Quarter",
            "quarter",
            "Quarterly",
            "quarterly",
        ]
        self.annual_params = ["a", "A", "Annual", "annual"]

    """-----------------------------------"""

    def create_browser(self, url=None):
        """
        :param url: The website to visit.
        :return: None
        """
        service = Service(executable_path=self.chrome_driver_path)
        self.browser = webdriver.Chrome(service=service, options=self.chrome_options)
        # Default browser route
        if url == None:
            self.browser.get(url=self.sec_annual_url)
        # External browser route
        else:
            self.browser.get(url=url)

    def clean_close(self) -> None:
        self.browser.close()
        self.browser.quit()

    """-----------------------------------"""

    def scroll_page(
        self,
        pixel_to_scroll: int = 500,
        element_to_scroll="",
        by_pixel: bool = True,
        by_element: bool = False,
    ) -> None:
        """
        :param element_to_scroll: Scroll to the specified element on the webpage.
        :returns: There is no data to return.
        """
        if by_pixel:
            self.browser.execute_script(f"window.scrollBy(0, {pixel_to_scroll})", "")

        if by_element:
            self.browser.execute_script(
                "arguments[0].scrollIntoView(true);", element_to_scroll
            )

    """-----------------------------------"""

    def get_webpage_dimensions(self):
        """
        Get the webpage width and height for the current url.
        """
        width = self.browser.execute_script("return window.outerWidth")
        height = self.browser.execute_script("return window.outerHeight")
        return width, height

    def read_data(
        self, xpath: str, wait: bool = False, _wait_time: int = 5, tag: str = ""
    ) -> str:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: (str) Text of the element.
        """

        if wait:
            try:
                data = (
                    WebDriverWait(self.browser, _wait_time)
                    .until(EC.presence_of_element_located((By.XPATH, xpath)))
                    .text
                )
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
            except NoSuchElementException:
                print(f"[Failed Xpath] {xpath}")
                return "N\A"
        else:
            try:
                data = self.browser.find_element("xpath", xpath).text
            except NoSuchElementException:
                data = "N\A"
        # Return the text of the element found.
        return data

    """-----------------------------------"""

    def click_button(
        self,
        xpath: str,
        wait: bool = False,
        _wait_time: int = 5,
        scroll: bool = False,
        tag: str = "",
    ) -> None:
        """
        :param xpath: Path to the web element.
        :param wait: Boolean to determine if selenium should wait until the element is located.
        :param wait_time: Integer that represents how many seconds selenium should wait, if wait is True.
        :return: None. Because this function clicks the button but does not return any information about the button or any related web elements.
        """

        if wait:
            try:
                element = WebDriverWait(self.browser, _wait_time).until(
                    EC.presence_of_element_located((By.XPATH, xpath))
                )
                # If the webdriver needs to scroll before clicking the element.
                if scroll:
                    self.browser.execute_script("arguments[0].click();", element)
                element.click()
            except TimeoutException:
                print(f"[Failed Xpath] {xpath}")
                if tag != "":
                    print(f"[Tag]: {tag}")
                raise NoSuchElementException("Element not found")
        else:
            element = self.browser.find_element("xpath", xpath)
            if scroll:
                self.browser.execute_script("arguments[0].click();", element)
            element.click()

    """
    Formatting
    """

    def format_basic(self, val) -> int:
        magnitudes = ["m", "b", "t"]
        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]
            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = int(float(val) * multi)

            return val
        except IndexError:
            return np.nan

    def format_dollar(self, val) -> float:
        magnitudes = ["m", "b", "t"]
        # Remove dollar sign from string if present.
        if "$" in val:
            val = val.replace("$", "")

        # Remove commas from string if present.
        if "," in val:
            val = val.replace(",", "")

        try:
            magnitude = val[-1]

            if magnitude in magnitudes:
                val = val[:-1]  # Remove suffix.
                if magnitude.lower() == "m":
                    multi = 1_000_000
                elif magnitude.lower() == "b":
                    multi = 1_000_000_000
                elif magnitude.lower() == "t":
                    multi = 1_000_000_000_000

                val = float(val) * multi

            try:
                return int(val)
            except ValueError:
                return float(val)
        except IndexError:
            return np.nan

    """------------------------------- Date Utilities -------------------------------"""
    """-------------------------------"""

    def get_date_difference(self, target_date: str, compare_date: str):
        """
        Description: Calculates the difference between the "target_date" and "compare_date".

        :param target_date: Main date.
        :param compare_date: Date to compare agains the main_date.
        :return: Integer
        """

        date_format = "%Y-%m-%d"

        # Turn string dates into datetime objects.
        target_date = dt.datetime.strptime(target_date, date_format)
        compare_date = dt.datetime.strptime(compare_date, date_format)

        # Check which date is larger. Subtract the smaller date from the larger date, to avoid negative values.
        if target_date > compare_date:
            delta = target_date - compare_date
        else:
            delta = compare_date - target_date
        difference = delta.days
        return difference

    """-------------------------------"""

    def add_days_to_date(self, target_date: str, days_to_add: int = 1):
        """
        :param target_date: The date to use for the calculations.
        :param days_to_add: Number of days to add to the "target_date".
        :return: Return the new data after the calculations.
        """
        # Convert the string to "datetime".
        date_format = "%m-%d"
        target_date = dt.datetime.strptime(target_date, date_format)

        # Add the number of days to the target_date.
        new_date = target_date + dt.timedelta(days=days_to_add)
        # Example: If the date is: 07-31 -> 2014-1900-08-01 00:00:00 || Get the next date "days_to_add" days after the target date.
        # Using the strftime function will now make the date.
        new_date = new_date.strftime(date_format)

        return new_date

    """-------------------------------"""

    def if_date_greater(self, target_date, compare_date):
        """
        :param target_date: The date that we are checking if it is greater or less than.
        :param compare_date: The date that the target_date is being compared against.
        return: Boolean. Will return True if the target_date is greater than the compare_date.
                Will return False if the target_date is less than the compare_date.
        """
        # Convert the strings into "datetime".
        date_format = "%m-%d"
        target_date = dt.datetime.strptime(target_date, date_format)
        compare_date = dt.datetime.strptime(compare_date, date_format)

        if target_date > compare_date:
            return True
        else:
            return False

    """------------------------------- Date Utilities -------------------------------"""

    def compare_dates(self, date1, date2, days_threshold: int = 10):
        """
        :param date1: A date that *only* contains the month and day.
        :param date2: A date that *only* contains the month and day.
        :param days_threshold: The number of days that are allowed between the dates.
        returns: Boolean that describes if the difference between date1 & date2 is less than "days_threshold".
                If it is greater than "days_threshold" it will return False. NOTE: The default is 10, but can be changed based on the users needs.
        """
        # Convert date strings into "datetime" objects.
        date1 = dt.datetime.strptime(date1, "%m-%d")
        date2 = dt.datetime.strptime(date2, "%m-%d")

        # Calculate the number of days between the 2 dates.
        # NOTE: We subtract the smaller date from the larger date to avoid negative delta.
        if date1 > date2:
            delta = date1 - date2
        else:
            delta = date2 - date1

        # Get the days from the delta.
        delta = delta.days

        # If the delta is less than the "days_threshold".
        if delta <= days_threshold:
            return True
        else:
            return False
