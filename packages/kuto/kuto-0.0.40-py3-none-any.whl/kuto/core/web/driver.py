"""
@Author: kang.yang
@Date: 2023/5/12 20:49
"""
import time

from playwright.sync_api import sync_playwright, expect

from kuto.utils.common import screenshot_util
from kuto.utils.log import logger


class PlayWrightDriver:

    def __init__(self, browserName: str, headless: bool = False, state: dict = None):
        self.browserName = browserName
        self.headless = headless

        self.playwright = sync_playwright().start()
        if browserName == 'firefox':
            self.browser = self.playwright.firefox.launch(headless=headless)
        elif browserName == 'webkit':
            self.browser = self.playwright.webkit.launch(headless=headless)
        else:
            self.browser = self.playwright.chromium.launch(headless=headless)
        if state:
            self.context = self.browser.new_context(storage_state=state, no_viewport=True)
        else:
            self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()

    def switch_tab(self, locator):
        logger.info("开始切换tab")
        start = time.time()
        with self.page.expect_popup() as popup_info:
            locator.click()
        self.page = popup_info.value
        end = time.time()
        logger.info(f"切换成功，耗时: {end - start}s")

    def visit(self, url):
        logger.info(f"访问页面: {url}")
        start = time.time()
        self.page.goto(url)
        end = time.time()
        logger.info(f"访问成功，耗时: {end - start}s")

    def storage_state(self, path=None):
        logger.info("保存浏览器状态信息")
        start = time.time()
        if not path:
            raise ValueError("路径不能为空")
        self.context.storage_state(path=path)
        end = time.time()
        logger.info(f"保存成功，耗时: {end - start}s")

    @property
    def page_content(self):
        """获取页面内容"""
        start = time.time()
        logger.info("获取页面内容")
        content = self.page.content()
        end = time.time()
        logger.info(f"获取成功: {content}，耗时: {end - start}s")
        return content

    def set_cookies(self, cookies: list):
        logger.info("添加cookie并刷新页面")
        start = time.time()
        self.context.add_cookies(cookies)
        self.page.reload()
        end = time.time()
        logger.info(f"操作成功，耗时: {end - start}s")

    def screenshot(self, file_name=None, with_time=True, delay=2):
        screenshot_util(self.page, file_name=file_name, with_time=with_time, delay=delay)

    def close(self):
        logger.info("关闭浏览器")
        start = time.time()
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()
        end = time.time()
        logger.info(f"关闭成功，耗时: {end - start}s")

    def assertTitle(self, title: str, timeout: int = 5):
        logger.info(f"断言页面标题等于: {title}")
        expect(self.page).to_have_title(title, timeout=timeout * 1000)

    def assertUrl(self, url: str, timeout: int = 5):
        logger.info(f"断言页面url等于: {url}")
        expect(self.page).to_have_url(url, timeout=timeout * 1000)

    def assertContent(self, text, count=3):
        logger.info(f"断言页面文本包括: {text}")
        url = self.page.url
        self.page.wait_for_url(url)  # 必须调用这个方法，不然获取content可能会报错
        result = False
        for item in range(count):
            page_content = self.page_content
            if text in page_content:
                result = True
                break
            time.sleep(1)
        assert result, f"页面内容不包含文本: {text}"


