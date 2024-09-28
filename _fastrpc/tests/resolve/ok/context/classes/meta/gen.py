def dynamic_class_creator(class_name: str, **attributes):
    """Decorator to create a class dynamically with specified attributes."""

    def decorator(cls):
        # Define a new class that inherits from the decorated class
        new_class = type(class_name, (cls,), attributes)

        # Prevent instantiation of the original class
        def init(self):
            raise TypeError(f"{cls.__name__} cannot be instantiated directly.")

        # Override the original class's __init__ method
        cls.__init__ = init
        return new_class

    return decorator


# Use the decorator to create a dynamic class
@dynamic_class_creator("DynamicClass", x=10, y=20)
class MyClass:
    def __init__(self):
        print("instance")


def dynamic_class_creator(class_name: str, **attributes):
    """Decorator to create a class dynamically with specified attributes."""

    def decorator(cls):
        # Define a new class that inherits from the decorated class
        new_class = type(class_name, (cls,), attributes)

        # Prevent instantiation of the original class
        def init(self):
            raise TypeError(f"{cls.__name__} cannot be instantiated directly.")

        # Override the original class's __init__ method
        cls.__init__ = init
        return new_class

    return decorator


# This will raise an error
try:
    instance = MyClass()  # Attempting to instantiate MyClass
except TypeError as e:
    print(e)  # Output: MyClass cannot be instantiated directly.

# Create an instance of the dynamically created class
# DynamicClassInstance = DynamicClass()
# print(DynamicClassInstance.x)  # Output: 10
# print(DynamicClassInstance.y)  # Output: 20
