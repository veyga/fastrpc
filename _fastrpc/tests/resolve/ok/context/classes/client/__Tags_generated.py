from fastrpc.client import as_rpc_result, RpcResult
from ..server.contexts import (
    Token,
    Pagination,
)
from typing import Awaitable


# TokenContext = ServerTokenContext
# PaginationContext = __ServerPaginationContext


class Tags:
    def __init__(self, *, token: Token):
        self.token = token
        self.__TAGS = ["A1", "A2", "B1", "B2", "B3"]

    def get_matching_tags(
        self,
        *,
        letter: str,
    ) -> Awaitable[RpcResult[list[str]]]:
        async def call_it():
            if letter == "C":
                raise ValueError("can't search for 'C'")
            return [tag for tag in self.__TAGS if tag.startswith(letter)]

        return as_rpc_result(call_it)()

    def get_matching_tags_paginated(
        self,
        *,
        pagination: Pagination,
        letter: str,
    ) -> Awaitable[RpcResult[list[str]]]:
        async def call_it():
            limit = pagination.limit
            return [tag for tag in self.__TAGS if tag.startswith(letter)][:limit]

        return as_rpc_result(call_it)()


__all__ = [
    "Tags",
]
