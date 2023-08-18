import os
import re
import time
import subprocess
import requests
import six
import uiautomator2 as u2

from kuto.utils.common import screenshot_util
from kuto.utils.exceptions import PkgIsNull, \
    DeviceNotFoundException, HealthCheckFail
from kuto.utils.log import logger


class AndroidDriver(object):

    def __init__(self, device_id=None, pkg_name=None):
        self.pkg_name = pkg_name
        if not self.pkg_name:
            raise PkgIsNull('应用包名不能为空')
        self.device_id = device_id
        if not self.device_id:
            raise DeviceNotFoundException('设备id不能为空')

        self.d = u2.connect(self.device_id)

        # check if atx is ready.
        try:
            self.d.reset_uiautomator("healthcheck")
        except:
            raise HealthCheckFail("设备健康检查失败!!!")

    def get_app_info(self, pkg_name=None):
        logger.info("获取应用信息")
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        info = self.d.app_info(pkg_name)
        end = time.time()
        logger.info(f'耗时: {end - start}s，{info}')
        return info

    def get_device_info(self):
        logger.info(f"获取设备信息")
        start = time.time()
        info = self.d.device_info
        end = time.time()
        logger.info(f'耗时: {end - start}s，{info}')
        return info

    @property
    def page_content(self):
        logger.info("获取页面xml")
        start = time.time()
        info = self.d.dump_hierarchy()
        end = time.time()
        logger.info(f'耗时: {end - start}s，{info[0:100]}...{info[100:]}')
        return info

    def assertActivity(self, activity_name: str, timeout=5):
        logger.info(f"断言 activity 等于 {activity_name}")
        assert self.d.wait_activity(activity_name, timeout=timeout)

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

    def uninstall_app(self, pkg_name=None):
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        logger.info(f"卸载应用")
        self.d.app_uninstall(pkg_name)
        end = time.time()
        logger.info(f"卸载成功，耗时: {end - start}s")

    @staticmethod
    def download_apk(src):
        """下载安装包"""
        start = time.time()
        if isinstance(src, six.string_types):
            if re.match(r"^https?://", src):
                logger.info(f'下载中...')
                file_path = os.path.join(os.getcwd(), src.split('/')[-1])
                r = requests.get(src, stream=True)
                if r.status_code != 200:
                    raise IOError(
                        "Request URL {!r} status_code {}".format(src, r.status_code))
                with open(file_path, 'wb') as f:
                    f.write(r.content)
                end = time.time()
                logger.info(f'下载成功: {file_path}，耗时: {end - start}s')
                return file_path
            elif os.path.isfile(src):
                return src
            else:
                raise IOError("static {!r} not found".format(src))

    def install_app(self, apk_path, auth=True, new=True, pkg_name=None):
        """
        安装应用，push改成adb命令之后暂时无法支持远程手机调用
        @param pkg_name: 应用包名
        @param apk_path: 安装包链接，支持本地路径以及http路径
        @param auth: 是否进行授权
        @param new: 是否先卸载再安装
        """
        start = time.time()
        logger.info(f"安装应用: {apk_path}")
        # 卸载
        if new is True:
            if pkg_name is None:
                pkg_name = self.pkg_name
            self.uninstall_app(pkg_name)

        # 下载
        source = self.download_apk(apk_path)

        # 把安装包push到手机上
        target = "/static/local/tmp/_tmp.apk"
        cmd = f'adb -s {self.device_id} push {source} {target}'
        subprocess.check_call(cmd, shell=True)

        # 安装
        cmd_list = ['pm', 'install', "-r", "-t", target]
        if auth is True:
            cmd_list.insert(4, '-g')
        logger.debug(f"{' '.join(cmd_list)}")
        cmd_str = f'adb -s {self.device_id} shell {" ".join(cmd_list)}'
        subprocess.check_call(cmd_str, shell=True)

        # 删除下载的安装包
        if 'http' in apk_path:
            os.remove(source)

        end = time.time()
        logger.info(f'安装成功，耗时: {end - start}s')

    def start_app(self, pkg_name=None, stop=True):
        """启动应用
        @param pkg_name: 应用包名
        @param stop: 是否先关闭应用再启动
        """
        logger.info(f"启动应用")
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        self.d.app_start(pkg_name, stop=stop, use_monkey=True)
        end = time.time()
        logger.info(f"启动成功，耗时: {end - start}s")

    def stop_app(self, pkg_name=None):
        logger.info("关闭应用")
        start = time.time()
        if not pkg_name:
            pkg_name = self.pkg_name
        self.d.app_stop(pkg_name)
        end = time.time()
        logger.info(f"关闭成功，耗时: {end - start}s")

    def screenshot(self, file_name=None, with_time=True, delay=2):
        screenshot_util(self.d, file_name=file_name, with_time=with_time,
                        delay=delay)

    def back(self):
        logger.info("返回上一页")
        start = time.time()
        self.d.press('back')
        end = time.time()
        logger.info(f"返回成功，耗时: {end - start}")

    def click(self, x, y):
        logger.info(f"点击坐标 : {x},{y}")
        start = time.time()
        self.d.click(x, y)
        end = time.time()
        logger.info(f'点击成功，耗时: {end - start}s')

    def click_alerts(self, alert_list: list):
        logger.info(f"点击弹窗: {alert_list}")
        start = time.time()
        with self.d.watch_context() as ctx:
            for alert in alert_list:
                ctx.when(alert).click()
            ctx.wait_stable()
        end = time.time()
        logger.info(f"点击成功，耗时: {end - start}")




