import pytest
from .client import Tags
from .server.contexts import Token, Pagination
from functools import partial


@pytest.mark.asyncio
async def test_classes():
    print("")
    api = Tags(token=Token("valid"))

    pagination = Pagination(2)
    a_tags = await api.get_matching_tags_paginated(pagination=pagination, letter="A")
    print(a_tags)

    use_pagination = partial(api.get_matching_tags_paginated, pagination=pagination)
    b_tags = await use_pagination(letter="B")
    print(b_tags)

    c_tags = await api.get_matching_tags(letter="C")
    print(c_tags)
