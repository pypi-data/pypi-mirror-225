import time
import typing

from uiautomator2 import UiObject
from uiautomator2.xpath import XPathSelector

from kuto.core.android.driver import AndroidDriver
from kuto.utils.exceptions import NoSuchElementException
from kuto.utils.log import logger


def dict_to_str(source_dict: dict):
    dict_str = '_'.join([f"{key}" for key, value in source_dict.items()])
    return f'{dict_str}_find_fail'


class AdrElem(object):
    """
    安卓元素定义
    """

    def __init__(self,
                 driver: AndroidDriver = None,
                 rid: str = None,
                 cname: str = None,
                 text: str = None,
                 xpath: str = None,
                 index: int = None):
        """
        @param driver: 安卓驱动，必填
        @param rid: resourceId定位
        @param cname: className定位
        @param text: text定位，这种定位方式比较慢
        @param xpath: xpath定位
        @param index: 定位出多个元素时，指定索引，从0开始
        """
        self._driver = driver

        self._kwargs = {}
        if rid is not None:
            self._kwargs["resourceId"] = rid
        if cname is not None:
            self._kwargs["className"] = cname
        if text is not None:
            self._kwargs["text"] = text
        if xpath:
            self._kwargs["xpath"] = xpath
        if index is not None:
            self._kwargs["instance"] = index

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    def get_element(self, timeout=5, screenshot=True):
        """
        增加截图的方法
        @param timeout: 每次查找时间
        @param screenshot
        @return:
        """
        start = time.time()
        _xpath = self._kwargs.get("xpath")
        if _xpath is not None:
            logger.info(f'查找控件: xpath={_xpath}')
        else:
            logger.info(f'查找控件: {self._kwargs}')
        _element = self._driver.d.xpath(_xpath) if \
            _xpath is not None else self._driver.d(**self._kwargs)

        if _element.wait(timeout=timeout):
            end = time.time()
            logger.info(f"查找成功，耗时: {end - start}s")
            return _element
        else:
            end = time.time()
            logger.info(f"查找失败，耗时: {end - start}s")
            if screenshot:
                self._driver.screenshot(dict_to_str(self._kwargs))
            raise NoSuchElementException(f"控件 {self._kwargs} 查找失败")

    def get_text(self, timeout=3):
        logger.info("获取控件文本属性")
        start = time.time()
        text = self.get_element(timeout=timeout).get_text()
        logger.debug(text)
        end = time.time()
        logger.info(f'耗时: {end - start}s, {text}')
        return text

    def exists(self, timeout=3):
        logger.info("检查控件是否存在")
        start = time.time()
        result = False
        try:
            self.get_element(timeout=timeout, screenshot=False)
        except:
            pass
        else:
            result = True
        finally:
            end = time.time()
            logger.info(f'耗时: {end - start}s, {result}')
            return result

    @staticmethod
    def _adapt_center(e: typing.Union[UiObject, XPathSelector],
                      offset=(0.5, 0.5)):
        """
        修正控件中心坐标
        """
        if isinstance(e, UiObject):
            return e.center(offset=offset)
        else:
            return e.offset(offset[0], offset[1])

    def click(self, timeout=5, screenshot=True):
        logger.info("点击控件")
        start = time.time()
        element = self.get_element(timeout=timeout,
                                   screenshot=screenshot)
        # 这种方式经常点击不成功，感觉是页面刷新有影响
        # element.click()
        x, y = self._adapt_center(element)
        self._driver.d.click(x, y)
        end = time.time()
        logger.info(f'点击成功，耗时: {end - start}s')

    def click_exists(self, timeout=3):
        logger.info("控件存在才点击")
        if self.exists(timeout=timeout):
            self.click()
            logger.info(f"点击成功")
        else:
            logger.info("控件不存在")

    def input(self, text):
        logger.info(f"输入文本: {text}")
        start = time.time()
        self.get_element().set_text(text)
        end = time.time()
        logger.info(f"输入成功，耗时: {end - start}s")

    def input_exists(self, text: str, timeout=3):
        logger.info(f"控件存在才输入: {text}")
        if self.exists(timeout=timeout):
            self.input(text)
            logger.info("输入成功")
        else:
            logger.info("控件不存在")

    def input_pwd(self, text):
        """密码输入框输入有时候用input输入不了"""
        logger.info(f"输入密码: {text}")
        start = time.time()
        self.get_element().click()
        self._driver.d(focused=True).set_text(text)
        end = time.time()
        logger.info(f'输入成功，耗时: {end - start}s')

    def clear(self):
        logger.info("清空输入框")
        start = time.time()
        self.get_element().clear_text()
        end = time.time()
        logger.info(f"清空成功，耗时: {end - start}s")

    def assertExists(self, timeout=3):
        logger.info("断言控件存在")
        status = self.exists(timeout=timeout)
        assert status, "控件不存在"

    def assertText(self, text, timeout=3):
        logger.info(f"断言控件文本属性包括: {text}")
        _text = self.get_text(timeout=timeout)
        assert text in _text, f"文本属性 {_text} 不包含 {text}"



