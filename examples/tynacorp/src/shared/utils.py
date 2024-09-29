""" Various utility functions/types """

import aiofiles
import json
import typer
from asyncio import iscoroutinefunction, run
from collections import defaultdict
from functools import wraps
from typing import Callable


class AsyncTyper(typer.Typer):
    """An async wrapper for 'typer' CLI commands"""

    event_handlers: defaultdict[str, list[Callable]] = defaultdict(list)

    def async_command(self, *args, **kwargs):
        def decorator(async_func):
            @wraps(async_func)
            def sync_func(*_args, **_kwargs):
                self.run_event_handlers("startup")
                try:
                    return run(async_func(*_args, **_kwargs))
                except Exception as e:  # noqa
                    raise e
                finally:
                    self.run_event_handlers("shutdown")

            self.command(*args, **kwargs)(sync_func)
            return async_func

        return decorator

    def add_event_handler(self, event_type: str, func: Callable) -> None:
        self.event_handlers[event_type].append(func)

    def run_event_handlers(self, event_type: str):
        for event in self.event_handlers[event_type]:
            if iscoroutinefunction(event):
                run(event())
            else:
                event()


async def load_and_parse_json(file_path: str):
    """Loads/parses a JSON file"""
    async with aiofiles.open(file_path, mode="r") as file:
        json_content = await file.read()
        return json.loads(json_content)
