import time


class JSUtil:

    def __init__(self, driver):
        self.__driver = driver

    def scroll_to_bottom(self):
        """
        Scrolls to the bottom of the page using JavaScript.
        """
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    def scroll_to_top(self):
        """
        Scrolls to the top of the page using JavaScript.
        """
        self.__driver.execute_script("window.scrollTo(0, 0);")

    def scroll_by(self, x, y):
        """
        Scrolls the page by a specified amount in the x and y directions from the current position.

        :param x: The number of pixels to scroll horizontally.
        :param y: The number of pixels to scroll vertically.
        """
        self.__driver.execute_script(f"window.scrollBy({x}, {y});")

    def scroll_into_view(self, element):
        """
        Scrolls the specified element into view using JavaScript.

        :param element: The WebElement to scroll into view.
        """
        self.__driver.execute_script("arguments[0].scrollIntoView(true);", element)

    def scroll_to_position(self, x, y):
        """
        Scrolls the page to a specific position using JavaScript.

        :param x: The horizontal position to scroll to.
        :param y: The vertical position to scroll to.
        """
        self.__driver.execute_script(f"window.scrollTo({x}, {y});")

    def click_element(self, element):
        """
        Clicks on a specified element using JavaScript.

        :param element: The WebElement to click.
        """
        self.__driver.execute_script("arguments[0].click();", element)

    def send_keys(self, element, value):
        """
        Sends keys to a specified element using JavaScript.

        :param element: The WebElement to send keys to.
        :param value: The value to send to the element.
        """
        self.__driver.execute_script("arguments[0].value = arguments[1];", element, value)

    def get_page_title(self):
        """
        Returns the title of the current page using JavaScript.

        :return: The title of the page.
        """
        return self.__driver.execute_script("return document.title;")

    def refresh_page(self):
        """
        Refreshes the current page using JavaScript.
        """
        self.__driver.execute_script("location.reload();")

    def go_back(self):
        """
        Navigates back to the previous page using JavaScript.
        """
        self.__driver.execute_script("window.history.back();")

    def go_forward(self):
        """
        Navigates forward to the next page using JavaScript.
        """
        self.__driver.execute_script("window.history.forward();")

    def get_bg_color(self, element):
        """ Retrieves the background color of a specified element using JavaScript."""
        return self.__driver.execute_script("return window.getComputedStyle(arguments[0]).backgroundColor;", element)

    def change_bg_color(self, element, color):
        """ Changes the background color of a specified element using JavaScript."""
        self.__driver.execute_script("arguments[0].style.backgroundColor = arguments[1];", element, color)

    def flash_element(self, element):
        """ Flashes a specified element by changing its background color multiple times."""
        bg_color = self.get_bg_color(element)
        for i in range(20):
            # Flash the element by changing its background color
            self.change_bg_color(element, 'lightgreen')
            time.sleep(0.05)
            self.change_bg_color(element, bg_color)
