class Singleton(type):
    """
    Metaclass implementing the Singleton design pattern.

    This metaclass ensures that a class has only one instance and provides
    a global point of access to that instance.

    Usage:
        class MyClass(metaclass=Singleton):
            # Your class definition

    Attributes:
        _instances (dict): A dictionary storing instances of Singleton classes.

    Methods:
        __call__(cls, *args, **kwargs):
            Override of the call behavior to create and return a single instance
            of the class if it doesn't exist, or return the existing instance.

    Examples:
        class SingletonClass(metaclass=Singleton):
            pass
        instance1 = SingletonClass()
        instance2 = SingletonClass()
        assert instance1 is instance2  # Both references point to the same instance.
    """
    _instances = {}

    def __call__(cls, *args, **kwargs):
        """
        Create and return a single instance of the class if it doesn't exist,
        or return the existing instance.

        Args:
            cls (class): The class being instantiated.
            *args: Positional arguments for the class constructor.
            **kwargs: Keyword arguments for the class constructor.

        Returns:
            object: An instance of the class.
        """
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
