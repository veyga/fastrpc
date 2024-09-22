import os
from enum import Enum


class Environment(Enum):
    TEST = "test"

    @classmethod
    def IS_TEST(cls) -> bool:
        return os.getenv("ENVIRONMENT") == cls.TEST.value

    @classmethod
    def getenvironment(cls) -> "Environment":
        """Gets the Environment value of the current environment"""
        return Environment(cls.getenv())

    @staticmethod
    def getenv() -> str:
        """Gets the str value of the current environment"""
        return os.getenv("ENVIRONMENT", "")
