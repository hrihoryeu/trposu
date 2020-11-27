class Major():
    def __init__(self):
        pass

    class Minor1():
        def __init__(self):
            print('I am class Minor1 and i opened')

        def say_hello(self):
            print('Hello')

    class Minor2():
        def __init__(self):
            print('I am class Minor2 and i opened')

        def say_goodbye(self):
            print('Good bye')

object1 = Major()
object2 = object1.Minor1()
object3 = object1.Minor2()

object2.say_hello()
object3.say_goodbye()