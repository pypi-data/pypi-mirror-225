"""
@Author: kang.yang
@Date: 2023/5/16 14:37
"""
import kuto

from page.web_page import IndexPage, LoginPage


# @kuto.feature("web测试demo")
# @kuto.story("PO模式")
# class TestPoDemo(kuto.Case):
#
#     def start(self):
#         self.ip = IndexPage(self.driver)
#         self.lp = LoginPage(self.driver)
#
#     @kuto.title("登录")
#     def test_login(self):
#         self.open()
#         self.ip.loginBtn.click()
#         self.lp.pwdLoginTab.click()
#         self.lp.userInput.input('13652435335')
#         self.lp.pwdInput.input('wz123456@QZD')
#         self.lp.licenseBtn.click()
#         self.lp.loginBtn.click()
#         self.lp.firstCompanyIcon.click()
#         self.lp.assertContent("查专利")
#         self.screenshot("首页")


@kuto.feature("web测试demo")
@kuto.story("普通模式")
class TestNormalDemo(kuto.Case):

    @kuto.title("登录")
    def test_login(self):
        self.open()
        kuto.logger.info(self.driver.page.url)
        self.sleep(5)
        self.elem(text='登录/注册').click()
        self.elem(text='帐号密码登录').click()
        self.elem(holder='请输入手机号码').input("13652435335")
        self.elem(holder='请输入密码').input("wz123456@QZD")
        self.elem(css="span.el-checkbox__inner", index=1).click()
        self.elem(text='立即登录').click()
        self.elem(xpath="(//img[@class='right-icon'])[1]").click()
        self.assertUrl("https://www-test.qizhidao.com/")
        self.elem(text='查专利').assertVisible()
        self.screenshot("首页")


if __name__ == '__main__':
    # 直接执行本文件，需要修改conf.yml中的platform
    kuto.main(
        platform="web",
        browser="chrome",
        host="https://www-test.qizhidao.com"
    )

