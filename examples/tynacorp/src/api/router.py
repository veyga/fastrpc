from fastapi import APIRouter

from .hello.router import (
    router as hello_router,
    METADATA as hello_router_metadata,
)
from . import PATH

METADATA = [
    *hello_router_metadata,
]

router = APIRouter(prefix=PATH)
router.include_router(hello_router)
