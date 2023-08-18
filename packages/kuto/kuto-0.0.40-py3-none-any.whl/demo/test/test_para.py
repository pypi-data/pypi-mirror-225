import kuto


LIST_DATA = [
    {"name": "李雷", "age": "33"},
    {"name": "韩梅梅", "age": "30"}
]


class TestParameter(kuto.Case):
    """
    原则是无论是哪种方式，返回的数据必须是list，用例都通过"param"进行调用
    """

    @kuto.data(LIST_DATA)
    def test_list(self, param):
        print(param)

    @kuto.file_data(file='static/data.json')
    def test_json(self, param):
        print(param)

    @kuto.file_data(file='static/data.yml', key='names')
    def test_yaml(self, param):
        print(param)

    @kuto.file_data(file='static/data.csv')
    def test_csv(self, param):
        print(param)

    @kuto.file_data(file='static/data.xlsx', row=1)
    def test_excel(self, param):
        kuto.logger.debug(param)


if __name__ == '__main__':
    kuto.main()
