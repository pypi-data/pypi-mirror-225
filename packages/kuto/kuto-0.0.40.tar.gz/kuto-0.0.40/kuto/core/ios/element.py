import time

from kuto.utils.exceptions import NoSuchElementException
from kuto.utils.log import logger
from kuto.core.ios.driver import IosDriver


def dict_to_str(source_dict: dict):
    dict_str = '_'.join([f"{key}" for key, value in source_dict.items()])
    return f'{dict_str}_find_fail'


class IosElem(object):
    """
    IOS原生元素定义
    """

    def __init__(self,
                 driver: IosDriver = None,
                 name: str = None,
                 label: str = None,
                 value: str = None,
                 text: str = None,
                 cname: str = None,
                 xpath: str = None,
                 index: int = None):
        """
        param driver,
        param name,
        param label,
        param value,
        param text,
        param cname,
        param xpath,
        param index: 索引
        """
        self._driver = driver

        self._kwargs = {}
        if name is not None:
            self._kwargs["name"] = name
        if label is not None:
            self._kwargs["label"] = label
        if value is not None:
            self._kwargs["value"] = value
        if text is not None:
            self._kwargs["text"] = text
        if cname is not None:
            self._kwargs["className"] = cname
        if index is not None:
            self._kwargs["index"] = index

        self._xpath = xpath

    def __get__(self, instance, owner):
        """po模式中element初始化不需要带driver的关键"""
        if instance is None:
            return None

        self._driver = instance.driver
        return self

    def get_element(self, timeout=5, screenshot=True):
        """
        针对元素定位失败的情况，抛出NoSuchElementException异常
        @param timeout:
        @param screenshot
        @return:
        """
        start = time.time()
        if self._xpath is not None:
            logger.info(f'查找控件: xpath={self._xpath}')
        else:
            logger.info(f'查找控件: {self._kwargs}')

        _element = self._driver.d.xpath(self._xpath) if \
            self._xpath else self._driver.d(**self._kwargs)

        try:
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
        except ConnectionError:
            logger.info('wda连接失败, 进行重连!!!')
            # 由于WDA会意外链接错误
            self._driver = IosDriver(self._driver.device_id, self._driver.pkg_name)
            time.sleep(5)

            logger.info('重连成功, 重新开始查找控件')
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
        """获取元素文本"""
        logger.info(f"获取空间文本属性")
        start = time.time()
        text = self.get_element(timeout=timeout).text
        end = time.time()
        logger.info(f"获取成功: {text}，耗时: {end - start}")
        return text

    def exists(self, timeout=3):
        """
        判断元素是否存在当前页面
        @param timeout:
        @return:
        """
        logger.info("检查控件是否存在")
        start = time.time()
        result = False
        try:
            self.get_element(timeout=timeout)
        except:
            result = False
        else:
            result = True
        finally:
            end = time.time()
            logger.info(f'耗时: {end - start}s, {result}')
            return result

    def click(self, timeout=5, screenshot=True):
        """
        单击
        @param: retry，重试次数
        @param: timeout，每次重试超时时间
        """
        start = time.time()
        logger.info('点击控件')
        self.get_element(timeout=timeout,
                         screenshot=screenshot).click()
        end = time.time()
        logger.info(f"点击成功，耗时: {end - start}s")

    def click_exists(self, timeout=3):
        logger.info(f"控件存在才点击")
        if self.exists(timeout=timeout):
            self.click()

    def clear(self):
        """清除文本"""
        logger.info("清除输入框文本")
        start = time.time()
        self.get_element().clear_text()
        end = time.time()
        logger.info(f"清除成功，耗时: {end - start}s")

    def input(self, text):
        """输入内容"""
        logger.info(f"输入文本：{text}")
        start = time.time()
        self.get_element().set_text(text)
        end = time.time()
        logger.info(f"输入成功，耗时: {end -start}s")

    def input_exists(self, text: str, timeout=3):
        logger.info(f"控件存在才输入: {text}")
        if self.exists(timeout=timeout):
            self.input(text)
            logger.info("输入成功")
        else:
            logger.info("控件不存在")

    def assertExists(self, timeout=3):
        logger.info("断言控件存在")
        status = self.exists(timeout=timeout)
        assert status, f"控件不存在"

    def assertText(self, text, timeout=3):
        logger.info(f"断言控件文本属性包括: {text}")
        _text = self.get_text(timeout=timeout)
        assert text in _text, f"文本属性 {_text} 不包含 {text}"




