import shutil
import subprocess
import time
import wda

from kuto.utils.exceptions import PkgIsNull, \
    DeviceNotFoundException, WDAStartFail
from kuto.utils.log import logger
from kuto.utils.common import screenshot_util
from kuto.core.ios.common import TideviceUtil


def _start_wda_xctest(udid: str, port, wda_bundle_id=None):
    xctool_path = shutil.which("tidevice")
    args = []
    if udid:
        args.extend(["-u", udid])
    args.append("wdaproxy")
    args.extend(["--port", str(port)])
    if wda_bundle_id is not None:
        args.extend(["-B", wda_bundle_id])
    p = subprocess.Popen([xctool_path] + args)
    time.sleep(3)
    if p.poll() is not None:
        raise WDAStartFail("wda启动失败，可能是手机未连接")


class IosDriver(object):

    def __init__(self, device_id: str = None, pkg_name: str = None, wda_url: str = None):
        if not pkg_name:
            raise PkgIsNull('应用包名不能为空')
        self.pkg_name = pkg_name
        if not device_id and not wda_url:
            raise DeviceNotFoundException('设备id和wda_url不能都为空')
        elif not device_id and wda_url:
            self.wda_url = wda_url
            self.d = wda.Client(self.wda_url)
            if self.d.is_ready():
                logger.info('wda已就绪')
            else:
                logger.info('wda连接失败')
        else:
            self.device_id = device_id
            self.port = self.device_id.split("-")[0][-4:]
            self.wda_url = f"http://localhost:{self.port}"
            self.d = wda.Client(self.wda_url)

            # check if wda is ready
            if self.d.is_ready():
                logger.info('wda已就绪')
            else:
                logger.info('wda未就绪, 现在启动')
                _start_wda_xctest(self.device_id, port=self.port)
                if self.d.is_ready():
                    logger.info('wda启动成功')
                else:
                    raise WDAStartFail('wda启动失败，可能是WebDriverAgent APP端证书失效!')

    def get_device_info(self):
        logger.info("获取设备信息")
        start = time.time()
        info = self.d.device_info()
        end = time.time()
        logger.info(f"{info}，耗时: {end - start}s")
        return info

    def get_current_app(self):
        logger.info("获取当前应用")
        start = time.time()
        info = self.d.app_current()
        end = time.time()
        logger.info(f"{info}，耗时: {end - start}s")

    @property
    def page_content(self):
        logger.info('获取页面xml内容')
        start = time.time()
        page_source = self.d.source(accessible=False)
        end = time.time()
        logger.info(f'耗时: {end - start}s，{page_source}')
        return page_source

    def install_app(self, ipa_url, new=True, pkg_name=None):
        """安装应用
        @param ipa_url: ipa链接
        @param new: 是否先卸载
        @param pkg_name: 应用包名
        @return:
        """
        logger.info(f"安装应用: {ipa_url}")
        start = time.time()
        if new is True:
            pkg_name = pkg_name if pkg_name else self.pkg_name
            self.uninstall_app(pkg_name)

        TideviceUtil.install_app(self.device_id, ipa_url)
        end = time.time()
        logger.info(f"安装成功，耗时: {end - start}s")

    def uninstall_app(self, pkg_name=None):
        start = time.time()
        pkg_name = pkg_name if pkg_name else self.pkg_name
        logger.info(f"卸载应用: {pkg_name}")
        TideviceUtil.uninstall_app(self.device_id, pkg_name)
        end = time.time()
        logger.info(f"卸载成功，耗时: {end - start}s")

    def start_app(self, pkg_name=None, stop=True):
        """启动应用
        @param pkg_name: 应用包名
        @param stop: 是否先停止应用
        """
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"启动应用: {pkg_name}")
        if stop is True:
            self.d.app_terminate(pkg_name)
        self.d.app_start(pkg_name)
        end = time.time()
        logger.info(f"启动成功，耗时: {end - start}s")

    def stop_app(self, pkg_name=None):
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"停止应用: {pkg_name}")
        self.d.app_terminate(pkg_name)
        end = time.time()
        logger.info(f"停止成功，耗时: {end - start}s")

    def back(self):
        """返回上一页"""
        start = time.time()
        logger.info("返回上一页")
        time.sleep(1)
        self.d.swipe(0, 100, 100, 100)
        end = time.time()
        logger.info(f"返回成功，耗时: {end - start}s")

    def screenshot(self, file_name=None, with_time=True, delay=2):
        screenshot_util(self.d, file_name=file_name, with_time=with_time, delay=delay)

    def click(self, x, y):
        logger.info(f"点击坐标: ({x}, {y})")
        start = time.time()
        self.d.appium_settings({"snapshotMaxDepth": 0})
        self.d.tap(x, y)
        self.d.appium_settings({"snapshotMaxDepth": 50})
        time.sleep(1)
        end = time.time()
        logger.info(f"点击成功，耗时: {end - start}s")

    def click_alerts(self, alert_list: list):
        """点击弹窗"""
        logger.info(f"点击弹窗: {alert_list}")
        start = time.time()
        try:
            self.d.alert.click(alert_list)
        except:
            pass
        end = time.time()
        logger.info(f"点击成功，耗时: {end - start}s")

    def assertContent(self, text, count=3):
        logger.info(f"断言页面文本包括: {text}")
        result = False
        for item in range(count):
            page_content = self.page_content
            if text in page_content:
                result = True
                break
            time.sleep(1)
        assert result, f"页面内容不包含文本: {text}"




