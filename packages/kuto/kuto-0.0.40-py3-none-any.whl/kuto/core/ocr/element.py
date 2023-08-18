import time

from kuto.utils.log import logger
from kuto.core.ocr.ocr_discern import OCRDiscern
from kuto.utils.exceptions import ElementNameEmptyException


class OCRElem(object):
    """ocr识别定位"""

    def __init__(self, driver=None, text: str = None, desc: str = None):
        self.driver = driver
        self.text = text
        if desc is None:
            raise ElementNameEmptyException("请设置控件名称")
        else:
            self._desc = desc

    def __get__(self, instance, owner):
        if instance is None:
            return None

        self.driver = instance.driver
        return self

    def exists(self, retry=3, timeout=1):
        logger.info(f'ocr识别文本: {self.text} 是否存在')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i+1}次查找:')
            self.driver.screenshot('SourceImage.png', with_time=False)
            res = OCRDiscern().get_coordinate(self.text)
            if isinstance(res, tuple):
                self.driver.screenshot(f'ocr识别定位-{self.text}')
                return True
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'ocr识别定位失败-{self.text}')
            return False

    def click(self, retry=3, timeout=1):
        logger.info(f'ocr点击文本: {self.text}')
        time.sleep(3)
        for i in range(retry):
            logger.info(f'第{i+1}次查找:')
            self.driver.screenshot('SourceImage.png', with_time=False)
            res = OCRDiscern().get_coordinate(self.text)
            if isinstance(res, tuple):
                logger.info(f'识别坐标为: {res}')
                self.driver.screenshot(f'ocr识别定位-{self.text}')
                self.driver.click(res[0], res[1])
                return
            time.sleep(timeout)
        else:
            self.driver.screenshot(f'ocr识别定位失败-{self.text}')
            raise Exception('通过OCR未识别指定文字或置信度过低，无法进行点击操作！')


if __name__ == '__main__':
    from kuto.core.android.driver import AndroidDriver

    driver = AndroidDriver()
    driver.pkg_name = 'com.qizhidao.clientapp'
    driver.start_app()
    elem = OCRElem(driver, '查企业', '查企业入口')
    elem.click()

