"""
@Author: kang.yang
@Date: 2023/5/13 10:16
"""
import time

from kuto.utils.exceptions import NoSuchElementException
from kuto.utils.log import logger
from kuto.core.web.driver import PlayWrightDriver
from playwright.sync_api import expect


def dict_to_str(source_dict: dict):
    dict_str = '_'.join([f"{key}" for key, value in source_dict.items()])
    return f'{dict_str}_find_fail'


class WebElem:
    """
    通过selenium定位的web元素
    """

    def __init__(self,
                 driver: PlayWrightDriver = None,
                 xpath: str = None,
                 css: str = None,
                 text: str = None,
                 holder: str = None,
                 index: int = None
                 ):
        """

        @param driver: 浏览器驱动
        @param xpath: xpath
        @param css: css selector
        @param text: 页面内容中的所有文本
        @param holder: 输入框默认文案
        """
        self._driver = driver
        self._xpath = xpath
        self._css = css
        self._text = text
        self._placeholder = holder
        self._index = index

    def __get__(self, instance, owner):
        """pm模式的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    def find_element(self):
        element = None
        if self._text:
            logger.info(f"根据文本定位: {self._text}")
            element = self._driver.page.get_by_text(self._text)
        if self._placeholder:
            logger.info(f"根据输入框默认文本定位: {self._placeholder}")
            element = self._driver.page.get_by_placeholder(self._placeholder)
        if self._css:
            logger.info(f"根据css selector定位: {self._css}")
            element = self._driver.page.locator(self._css)
        if self._xpath:
            logger.info(f"根据xpath定位: {self._xpath}")
            element = self._driver.page.locator(self._xpath)
        if self._index:
            element = element.nth(self._index)
        return element

    def fail_handler(self, screenshot=True):
        logger.info("查找失败")
        if screenshot:
            self._driver.screenshot("查找失败")
        raise NoSuchElementException("查找失败")

    def click(self, timeout=10, screenshot=True):
        logger.info("点击控件")
        start = time.time()
        try:
            self.find_element().click(timeout=timeout*1000)
            end = time.time()
            logger.info(f"点击成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"点击失败，耗时: {end -start}")
            self.fail_handler(screenshot=screenshot)

    def input(self, text, timeout=10):
        logger.info(f"输入文本: {text}")
        start = time.time()
        try:
            self.find_element().fill(text, timeout=timeout*1000)
            end = time.time()
            logger.info(f"输入成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"输入失败，耗时: {end - start}")
            self.fail_handler()

    def check(self, timeout=10):
        logger.info("选择选项")
        start = time.time()
        try:
            self.find_element().check(timeout=timeout*1000)
            end = time.time()
            logger.info(f"选择成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"选择失败，耗时: {end - start}")
            self.fail_handler()

    def select(self, value: str, timeout=10):
        logger.info("下拉选择")
        start = time.time()
        try:
            self.find_element().select_option(value, timeout=timeout*1000)
            end = time.time()
            logger.info(f"选择成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"选择失败，耗时: {end - start}")
            self.fail_handler()

    def text(self):
        logger.info("获取控件文本属性")
        start = time.time()
        try:
            text = self.find_element().text_content()
            end = time.time()
            logger.info(f"获取成功，耗时: {end - start}s")
            return text
        except:
            end = time.time()
            logger.info(f"获取失败，耗时:{end - start}s")
            self.fail_handler()

    def assertVisible(self):
        logger.info("断言控件可见")
        start = time.time()
        try:
            expect(self.find_element()).to_be_visible()
            end = time.time()
            logger.info(f"断言成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"断言失败，耗时: {end - start}s")
            self.fail_handler()

    def assertHidden(self):
        logger.info("断言控件被隐藏")
        start = time.time()
        try:
            expect(self.find_element()).to_be_hidden()
            end = time.time()
            logger.info(f"断言成功，耗时: {end -start}s")
        except:
            end = time.time()
            logger.info(f"断言失败，耗时: {end- start}s")
            self.fail_handler()

    def assertTextContain(self, text: str):
        logger.info(f"断言控件包含文本: {text}")
        start = time.time()
        try:
            expect(self.find_element()).to_contain_text(text)
            end = time.time()
            logger.info(f"断言成功，耗时: {end - start}s")
        except:
            end = time.time()
            logger.info(f"断言失败，耗时: {end - start}s")
            self.fail_handler()

    def assertTextEqual(self, text: str):
        logger.info(f"断言控件文本等于: {text}")
        start = time.time()
        try:
            expect(self.find_element()).to_have_text(text)
            end = time.time()
            logger.info(f"断言成功，耗时: {end - start}")
        except:
            end = time.time()
            logger.info(f"断言失败，耗时: {end - start}")
            self.fail_handler()


class FraElem(WebElem):

    def __init__(self, driver: PlayWrightDriver = None, frame: str = None, xpath: str = None, css: str = None,
                 text: str = None, holder: str = None, index: int = None):
        """

        @param driver: 浏览器驱动
        @type frame: frame定位方式，使用正常的css定位方式即可
        @param xpath: 根据xpath进行定位
        @param css: 根据css selector进行定位
        @param text: 根据标签的文本定位
        @param holder: 根据输入框的placeholder定位
        """
        super().__init__(driver, xpath, css, text, holder, index)
        self._driver = driver
        self._frame_loc = frame
        self._xpath = xpath
        self._css = css
        self._text = text
        self._placeholder = holder
        self._index = index

    def find_element(self):
        element = None
        if self._text:
            logger.info(f"根据文本定位: {self._text}")
            element = self._driver.page.frame_locator(self._frame_loc).get_by_text(self._text)
        if self._placeholder:
            logger.info(f"根据输入框默认文本定位: {self._placeholder}")
            element = self._driver.page.frame_locator(self._frame_loc).get_by_placeholder(self._placeholder)
        if self._css:
            logger.info(f"根据css定位: {self._css}")
            element = self._driver.page.frame_locator(self._frame_loc).locator(self._css)
        if self._xpath:
            logger.info(f"根据xpath定位: {self._xpath}")
            element = self._driver.page.frame_locator(self._frame_loc).locator(self._xpath)
        if self._index:
            element = element.nth(self._index)
        return element
