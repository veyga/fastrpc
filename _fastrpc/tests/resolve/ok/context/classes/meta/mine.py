from typing import Any, Dict, List, final
from pydantic.dataclasses import dataclass
from abc import ABC, abstractmethod


def remote_type(namespace: str = "root"):
    return final(dataclass)


@remote_type(namespace="tags")
class MyContext:
    token: str


class RemoteProcedureClassMeta(type):
    def __new__(cls, name, bases, attrs):
        print(cls, name, bases, attrs)
        attrs["greeting"] = "hey"
        return super().__new__(cls, name, bases, attrs)


def remote_class(namespace: str = "root"):
    def inner(cls):
        class NewClass(cls, metaclass=RemoteProcedureClassMeta):
            pass

        return final(NewClass)

    return inner


def remote_method():
    """Marks a method as a remote_method"""

    def inner(fn):
        def innr(*args, **kwargs):
            return fn(*args, **kwargs)

        return innr

    return inner


@remote_class(namespace="tags")
class TagsAPI:
    def __init__(self, context: MyContext):
        """Define any context needed for interacting with the remote_class"""
        assert context.token == "valid"
        self.context = context
        self.TAGS = ["A1", "A2", "A3"]

    @remote_method()
    async def get_matching_tags(self, *, x: str) -> List[str]:
        return [t for t in self.TAGS if x in t]

    @remote_method()
    async def get_matching_tags_paginated(self, *, x: str) -> List[str]:
        return [t for t in self.TAGS if x in t]


class Sup(TagsAPI):
    def sup(self):
        print("sup")


token = MyContext(token="valid")
api = TagsAPI(token)
# print(token)

ss = Sup(token)
ss.sup()


@remote_type()
class X(MyContext):
    name: str


x = X("asdf", "y")
print(x)
