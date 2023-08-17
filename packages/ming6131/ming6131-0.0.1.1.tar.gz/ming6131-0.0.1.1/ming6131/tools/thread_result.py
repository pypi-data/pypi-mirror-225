from threading import Thread
import time

'''
执行多线程并获取线程返回值
'''


class MyThread(Thread):

    def __init__(self, function, arg):
        Thread.__init__(self)
        self.result = None
        self.function = function
        self.arg = arg

    def run(self):
        self.result = self.function(self.arg)

    def get_result(self):
        return self.result


if __name__ == '__main__':

    ''' 示例 '''
    def foo(number):
        time.sleep(3)
        return number

    # 如果不用面向对象的方法，应该这样使用
    # t1 = Thread(target=func, args=("周杰伦",))  # target 指定一个任务函数，args 指定参数，必须是元组

    thd1 = MyThread(foo, 3)
    thd2 = MyThread(foo, 5)
    thd1.start()
    thd2.start()
    thd1.join()     # 等待线程执行完毕
    thd2.join()
    print(thd1.get_result())
    print(thd2.get_result())
