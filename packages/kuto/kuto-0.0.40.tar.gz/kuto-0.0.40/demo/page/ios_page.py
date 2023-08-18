"""
@Author: kang.yang
@Date: 202
3/8/1 16:27
"""
from kuto import Page, IosElem as Elem


class IndexPage(Page):
    """首页"""
    adBtn = Elem(text='close white big')
    myTab = Elem(text='我的')


class MyPage(Page):
    """我的页"""
    settingBtn = Elem(text='settings navi')
