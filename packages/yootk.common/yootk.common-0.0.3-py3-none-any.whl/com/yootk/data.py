RESOURCE = '沐言科技：yootk.com' # 全局变量
class Book: # 图书类
    def __init__(self, **kwargs): # 构造方法
        self.__name = kwargs.get('name') # 属性初始化
        self.__author = kwargs.get('author') # 属性初始化
    def __str__(self): # 获取对象信息
        return f'【图书】名称：{self.__name}、作者：{self.__author}'
class Press: # 出版社
    def publish(self, book): # 图书出版
        print(book) # 获取对象信息
