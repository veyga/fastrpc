import pytest
from .mine import Tags
from typing import Any, Iterable, Optional

# def remote_procedure_class(dependencies: Optional[Iterable] = None):
#   def inner(cls: Any) -> Any:
#       """Class decorator to add a 'name' field to the class."""
#       cls.name = None  # You can also set a default value here
#       return cls
#   return inner

# @remote_procedure_class()
# class ExampleClass:
#     def __init__(self, value: int):
#         self.value = value

# @remote_procedure_class()
# class AnotherClass:
#     def __init__(self, description: str):
#         self.description = description

# # Usage
# example = ExampleClass(10)
# another = AnotherClass("This is a test.")

# # Setting the 'name' field
# example.name = "Example Instance"
# another.name = "Another Instance"


@pytest.mark.asyncio
async def test_meta():
    print("")
    x = Tags()
    print(x.dependencies)
    print(x)
