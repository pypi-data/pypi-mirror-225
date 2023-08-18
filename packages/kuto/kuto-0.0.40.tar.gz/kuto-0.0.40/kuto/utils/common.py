"""
@Author: kang.yang
@Date: 2023/8/1 18:21
"""
import time
import os
import allure
from kuto.utils.log import logger
from kuto.utils.exceptions import ScreenFailException


def screenshot_util(driver, file_name=None, with_time=True, delay=2):
    """
    截图并保存到预定路径
    @param driver
    @param with_time: 是否带时间戳
    @param file_name: foo.png or fool
    @param delay：截图前的等待时间
    @return:
    """
    logger.info("开始截图")
    start = time.time()
    if delay:
        logger.info(f'等待 {delay}s')
        time.sleep(delay)  # 为了截图前页面更稳定一点
    if not file_name:
        raise ValueError("文件名不能为空")

    # 截图并保存到当前目录的image文件夹中
    relative_path = "image"
    try:
        # 把文件名处理成test.png的样式
        if "." in file_name:
            file_name = file_name.split(r".")[0]
        if os.path.exists(relative_path) is False:
            os.mkdir(relative_path)
        if with_time:
            time_str = time.strftime(f"%Y%m%d%H%M%S")
            file_name = f"{time_str}_{file_name}.png"
        else:
            file_name = f'{file_name}.png'

        file_path = os.path.join(relative_path, file_name)
        # logger.info(f"save to: {os.path.join(relative_path, file_name)}")
        if getattr(driver, "info", None):
            driver.screenshot(file_path)
        else:
            driver.screenshot(path=file_path)
        # 上传allure报告
        allure.attach.file(
            file_path,
            attachment_type=allure.attachment_type.PNG,
            name=f"{file_name}",
        )
    except Exception as e:
        raise ScreenFailException(f"截图失败: \n{str(e)}")
    finally:
        end = time.time()
        logger.info(f"截图完成，保存至: {os.path.join(relative_path, file_name)}，耗时: {end - start}s")
