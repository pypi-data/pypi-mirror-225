import kuto


if __name__ == '__main__':
    # 主程序入口

    # 执行接口用例
    kuto.main(
        platform="api",
        host='https://app-pre.qizhidao.com',
        path='tests/test_api.py'
    )

    # # 执行安卓用例
    # kuto.main(
    #     platform="android",
    #     did='UJK0220521066836',
    #     pkg='com.qizhidao.clientapp',
    #     path='test/test_adr.py'
    # )

    # 执行ios用例
    # kuto.main(
    #     platform="ios",
    #     did='00008101-000E646A3C29003A',
    #     pkg='com.qizhidao.company',
    #     path='test/test_ios.py'
    # )

    # 执行web用例
    # kuto.main(
    #     platform="web",
    #     browser="chrome",
    #     host='https://www.qizhidao.com/',
    #     path='test/test_web.py',
    # )
