# @remote_procedure_class(requires=[Token])
# class Tags:

#     # TODO how to handle default arguments
#     # TODO assert that the return type is a primitive or remote_procedure_type

#     @remote_method()
#     async def get_matching_tags(self, x: str) -> List[str]:
#         return [t for t in TAGS if x in t]

#     @remote_method(requires=[Pagination])
#     async def get_matching_tags_paginated(self, x: str) -> List[str]:
#         # self should have 'token' and 'pagination' fields
#         return [t for t in TAGS if x in t]

#     @remote_method(requires=[Pagination])
#     async def get_other_tags(self) -> List[str]:
#         # self should have 'token' and 'pagination' fields
#         return TAGS
