#!/usr/bin/env python3

import asyncio
import functools
import logging
import sys
from asyncio.subprocess import PIPE, create_subprocess_exec
from collections.abc import Callable
from contextlib import suppress
from dataclasses import dataclass
from functools import partial
from itertools import count

import asyncssh

from minimon.server import Context, Singleton, serve


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


class GlobalMonitorContext(Context, metaclass=Singleton):
    ...


@dataclass
class Host:
    name: str
    ip_address: None | str = None
    ssh_name: None | str = None
    ssh_key_file: None | str = None
    ssh_key_passphrase_cmd: None | str = None
    ssh_port: None | int = None

    def __str__(self):
        return self.name


# https://realpython.com/primer-on-python-decorators/#syntactic-sugar
def view(arg_name, arg_values):
    def decorator_view(afunc: Callable[[], int]):
        @functools.wraps(afunc)
        async def wrapper_view(*args: object, **kwargs: object) -> object:
            generator = afunc(*args, **kwargs)
            while True:
                try:
                    yield await anext(generator)
                except StopAsyncIteration:
                    log().info(f"StopAsyncIteration in {afunc.__name__}")
                    break
                except Exception:
                    log().exception("Unhandled exception in view generator:")

        fn_name = afunc.__name__
        for arg_value in arg_values:
            GlobalMonitorContext().add(
                f"{fn_name}-{arg_value}", wrapper_view(**{arg_name: arg_value})
            )

    return decorator_view


class HostConnection:
    def __init__(self, host: Host, log_fn) -> None:
        self.host_info = host
        self.log_fn = log_fn
        self.ssh_connection: None | asyncssh.SSHClientConnection = None

    async def __aenter__(self) -> "HostConnection":
        if self.host_info.ssh_name:
            self.ssh_connection = await asyncssh.connect(
                self.host_info.ip_address or self.host_info.name,
                port=self.host_info.ssh_port or (),
                username=self.host_info.ssh_name,
                # client_keys=[pkey],
            )

        return self

    async def __aexit__(self, *args: object) -> bool:
        if self.ssh_connection:
            self.ssh_connection.close()
        return True

    async def execute(self, command):
        if self.ssh_connection:

            def clean_lines(raw_line: str, log_widget) -> str:
                line = raw_line.strip("\n")
                log_widget.write_line(line)
                return line

            process = await self.ssh_connection.create_process(command)
            stdout, stderr, return_code = await asyncio.gather(
                self.log_fn(process.stdout, clean_lines),
                self.log_fn(process.stderr, clean_lines),
                process.wait(),
            )
            return stdout, stderr, return_code.returncode
        else:

            def clean_bytes(raw_line: bytes, log_widget) -> str:
                line = raw_line.decode().strip("\n")
                log_widget.write_line(line)
                return line

            process = await create_subprocess_exec(command, stdout=PIPE, stderr=PIPE)
            stdout, stderr, return_code = await asyncio.gather(
                self.log_fn(process.stdout, clean_bytes),
                self.log_fn(process.stderr, clean_bytes),
                process.wait(),
            )
            return stdout, stderr, return_code


async def process_output(host: Host, command, when: str):
    async def listen(log_widget, stream, clean_fn):
        return [clean_fn(raw_line, log_widget) async for raw_line in stream]

    logger = GlobalMonitorContext().current_logger()
    iterations = None

    async with HostConnection(host, partial(listen, logger)) as connection:
        for iteration in count():
            if iterations is not None and iteration >= iterations:
                break

            log().info("start task %r: %d", command, iteration)

            stdout, stderr, return_code = await connection.execute(command)

            log().info("task %r: %d, returned %d", command, iteration, return_code)

            yield stdout

            await asyncio.sleep(int(when))


async def iterate(**generator_defs):
    async def bundle(coro):
        async for result in coro:
            yield coro, result

    def task_from(name, coro):
        return asyncio.create_task(anext(bundle(coro)), name=name)

    tasks = set(task_from(name, coro) for name, coro in generator_defs.items())

    while tasks:
        done, tasks = await asyncio.wait(fs=tasks, return_when=asyncio.FIRST_COMPLETED)
        for event in done:
            with suppress(StopAsyncIteration):
                coro, result = event.result()
                name = event.get_name()
                tasks.add(task_from(name, coro))
                yield name, result


class Monitor:
    def __init__(self, name: str, log_level="INFO") -> None:
        self.name = name
        self.log_level = log_level

    def __enter__(self) -> "Monitor":
        return self

    def __exit__(self, *args: object) -> bool:
        if sys.exc_info() != (None, None, None):
            raise

        serve(GlobalMonitorContext(), self.log_level)
        return True


# with suppress(FileNotFoundError):
# with open(CONFIG_FILE) as config_file:
# config = yaml.load(config_file, yaml.Loader)
# print(config)
