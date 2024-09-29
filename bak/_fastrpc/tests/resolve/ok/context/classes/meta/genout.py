import ast
import astor


def dynamic_class_creator(class_name: str, **attributes):
    """Decorator to create a class dynamically with specified attributes using AST."""

    def decorator(cls):
        # Prevent instantiation of the original class
        def init(self):
            raise TypeError(f"{cls.__name__} cannot be instantiated directly.")

        cls.__init__ = init

        # Create a new class definition using AST
        new_class = create_dynamic_class(class_name, **attributes)

        # Write the new class to a file
        write_class_to_file(new_class)

        return cls  # Return the original class

    return decorator


def create_dynamic_class(class_name: str, **attributes):
    """Create a dynamic class using AST with default argument values."""
    # Define the __init__ method with type annotations and keyword-only arguments
    init_args = [
        ast.arg(arg=name, annotation=ast.Name(id=typ.__name__, ctx=ast.Load()))
        for name, typ in attributes.items()
    ]

    # Create default values for the arguments
    init_defaults = [
        ast.Constant(
            value="base" if typ is str else get_default_value(typ), ctx=ast.Load()
        )
        for typ in attributes.values()
    ]

    # Init body that assigns the parameters to instance variables
    init_body = [
        ast.Assign(
            targets=[
                ast.Attribute(
                    value=ast.Name(id="self", ctx=ast.Load()),
                    attr=name,
                    ctx=ast.Store(),
                )
            ],
            value=ast.Name(id=name, ctx=ast.Load()),
        )
        for name in attributes.keys()
    ]

    init_func = ast.FunctionDef(
        name="__init__",
        args=ast.arguments(
            args=[ast.arg(arg="self", annotation=None)] + init_args,
            vararg=None,
            kwonlyargs=[],
            kw_defaults=init_defaults,
            kwarg=None,
            defaults=[],
        ),
        body=init_body,
        decorator_list=[],
    )

    # Create the class
    class_def = ast.ClassDef(
        name=class_name, bases=[], body=[init_func], decorator_list=[]
    )

    return class_def


def get_default_value(typ):
    """Return a sensible default value based on the type."""
    if typ is int:
        return 0
    elif typ is float:
        return 0.0
    elif typ is bool:
        return False
    else:
        return None  # Fallback for other types


def write_class_to_file(class_def):
    """Writes the AST of the class to a Python file."""
    # Convert the AST to code
    class_code = astor.to_source(class_def)

    # Define the filename
    filename = f"{class_def.name.lower()}.py"

    with open(filename, "w") as f:
        f.write(class_code)


# Use the decorator to create a dynamic class
@dynamic_class_creator("DynamicClassKWWWW", x=int, y=str)
class MyClass:
    pass


# # This will raise an error
# try:
#     instance = MyClass()  # Attempting to instantiate MyClass
# except TypeError as e:
#     print(e)  # Output: MyClass cannot be instantiated directly.

# Now you can import DynamicClass from the generated file
