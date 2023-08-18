import kuto

from page.ios_page import IndexPage, MyPage


class TestPoDemo(kuto.Case):

    def start(self):
        self.ip = IndexPage(self.driver)
        self.mp = MyPage(self.driver)

    def test_go_setting(self):
        self.ip.myTab.click()
        self.mp.settingBtn.click()
        self.mp.assertContent("设置")


class TestNormalDemo(kuto.Case):

    def test_go_setting(self):
        self.elem(text='我的').click()
        self.elem(text="settings navi").click()
        self.assertContent("设置")
        self.screenshot("设置页")


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform="ios",
        did='00008101-000E646A3C29003A',
        pkg='com.qizhidao.company',
        auto_start=True)

