from fastrpc import dynamic_class_creator


# Use the decorator to create a dynamic class
@dynamic_class_creator("DynamicClass", x=int, y=str)
class MyClass:
    pass
