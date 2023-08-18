import unittest
from neuronautics.utils.singleton import Singleton


class TestSingleton(unittest.TestCase):
    def test_singleton(self):
        class A(metaclass=Singleton):
            pass

        instance1 = A()
        instance2 = A()
        self.assertEqual(instance1, instance2)


if __name__ == '__main__':
    unittest.main()
