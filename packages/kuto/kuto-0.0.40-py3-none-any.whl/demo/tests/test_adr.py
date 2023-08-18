import kuto

from page.adr_page import HomePage, MyPage, SettingPage


@kuto.feature("安卓测试demo")
@kuto.story("PO模式")
class TestPODemo(kuto.Case):

    def start(self):
        self.hp = HomePage(self.driver)
        self.mp = MyPage(self.driver)
        self.sp = SettingPage(self.driver)

    @kuto.title("从首页进入设置页")
    def test_go_setting(self):
        self.hp.myTab.click(timeout=10)
        self.mp.settingBtn.click()
        self.sp.assertActivity(
            '.me.MeSettingActivity')
        self.sp.screenshot("设置页")


@kuto.feature("安卓测试demo")
@kuto.story("普通模式")
class TestNormalDemo(kuto.Case):

    @kuto.title("从首页进入设置页")
    def test_go_setting(self):
        self.elem(xpath='//*[@resource-id="com.qizhidao.clientapp:id/ll'
                        'BottomTabs"]/android.widget.FrameLayout[4]').click(timeout=10)
        self.elem(rid='com.qizhidao.clientapp:id/me_top_bar_setting_iv').click()
        self.assertContent("设置")
        self.screenshot("设置页")


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform='android',
        did='UJK0220521066836',
        pkg='com.qizhidao.clientapp')


