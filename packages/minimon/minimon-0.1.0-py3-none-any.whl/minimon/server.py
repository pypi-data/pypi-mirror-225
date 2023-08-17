#!/usr/bin/env python3

"""Monitor I/O"""

import asyncio
import contextvars
import logging
import signal
import threading
from collections.abc import Callable, MutableMapping
from itertools import count
from pathlib import Path

from rich.logging import RichHandler
from textual import on
from textual.app import App, ComposeResult
from textual.containers import VerticalScroll
from textual.message import Message
from textual.widgets import Footer, Header, Log, Pretty, RichLog, Static

from minimon.logging_utils import setup_logging

CONFIG_FILE = Path("~/.config/monitor.io/monitor.io.yaml").expanduser()


def log() -> logging.Logger:
    """Logger for this module"""
    return logging.getLogger("minimon")


class Context:
    def __init__(self):
        self.things = {}
        self.log_widgets = {}
        self.logger_context = contextvars.ContextVar("logger_context")

    def add(self, name, generator):
        self.things[name] = generator

    def current_logger(self):
        return self.log_widgets[self.logger_context.get()]

    def set_current_logger(self, name, log_widget):
        self.logger_context.set(name)
        self.log_widgets[name] = log_widget


class RichLogHandler(RichHandler):
    def __init__(self, widget: RichLog):
        super().__init__(
            # show_time = False,
            # omit_repeated_times = False,
            # show_level = False,
            show_path=False,
            # enable_link_path = False,
            markup=False,
            # rich_tracebacks = False,
            # tracebacks_width: Optional[int] = None,
            # tracebacks_extra_lines: int = 3,
            # tracebacks_theme: Optional[str] = None,
            # tracebacks_word_wrap: bool = True,
            # tracebacks_show_locals: bool = False,
            # tracebacks_suppress: Iterable[Union[str, ModuleType]] = (),
            # locals_max_length: int = 10,
            # locals_max_string: int = 80,
            # log_time_format = "[%x %X]",
            # keywords= None,
        )
        self.widget: RichLog = widget

    def emit(self, record: logging.LogRecord) -> None:
        message = self.format(record)
        message_renderable = self.render_message(record, message)
        traceback = None
        log_renderable = self.render(
            record=record, traceback=traceback, message_renderable=message_renderable
        )
        self.widget.write(log_renderable)


class TaskWidget(Static):
    def compose(self) -> ComposeResult:
        yield Pretty({}, classes="box")
        yield Log(classes="box")


class MiniMoni(App[None]):
    """Terminal monitor for minimon"""

    CSS_PATH = "minimon.css"

    def __init__(self, context) -> None:
        super().__init__()
        self._widget_container = VerticalScroll()
        self.context = context

    def compose(self) -> ComposeResult:
        yield Header(show_clock=True)
        yield Footer()
        yield self._widget_container
        yield RichLog(
            # max_lines=None,
            # min_width=78,
            # wrap=False,
            # highlight=True,
            # markup=True,
            # auto_scroll=True,
            # name=None,
            # id=None,
            # classes=None,
            # disabled=False
        )

    @staticmethod
    async def task(name, task_fn, context: Context, widget: TaskWidget, update, cleanup):
        try:
            log().info("task %r started", task_fn)
            context.set_current_logger(name, widget.query_one(Log))
            async for data in task_fn:
                update(data)

        except Exception:
            log().exception("exception in %r", task_fn)
        finally:
            log().info("task %r terminated", task_fn)
            await cleanup()

    async def create_widget(self, title) -> TaskWidget:
        await self._widget_container.mount(widget := TaskWidget())
        widget.border_title = title
        return widget

    async def remove_widget(self, widget: TaskWidget) -> None:
        await widget.remove()

    async def add_task(self, name, task) -> TaskWidget:
        widget = await self.create_widget(name)
        asyncio.ensure_future(
            self.task(
                name,
                task,
                self.context,
                widget,
                widget.query_one(Pretty).update,
                lambda: self.remove_widget(widget),
            )
        )
        return widget

    async def on_mount(self) -> None:
        """UI entry point"""

        log().handlers = [RichLogHandler(self.query_one(RichLog))]

        for name, generator in self.context.things.items():
            await self.add_task(name, generator)

    @on(Message)
    async def on_msg(self, *event: str) -> None:
        """Generic message handler"""
        # log().debug("Event: %s", event)

    async def exe(self, on_exit: Callable[[], None]) -> None:
        """Execute and quit application"""
        try:
            await self.run_async()
        finally:
            on_exit()


def terminate(terminator: threading.Event) -> None:
    """Sends a signal to async tasks to tell them to stop"""
    try:
        terminator.set()
        for task in asyncio.all_tasks():
            task.cancel()
        asyncio.get_event_loop().stop()
    except Exception:  # pylint: disable=broad-except
        log().exception("terminate:")


def install_signal_handler(loop: asyncio.AbstractEventLoop, on_signal: Callable[[], None]) -> None:
    """Installs the CTRL+C application termination signal handler"""
    for signal_enum in [signal.SIGINT, signal.SIGTERM]:
        loop.add_signal_handler(signal_enum, on_signal)


class Singleton(type):
    """Yes, a Singleton"""

    _instances: MutableMapping[type, object] = {}

    def __call__(cls: "Singleton", *args: object, **kwargs: object) -> object:
        """Creates an instance if not available yet, returns it"""
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]


def serve(context: Context, log_level="INFO") -> None:
    """Synchronous entry point"""
    setup_logging(log_level)

    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    terminator = threading.Event()

    asyncio.ensure_future(MiniMoni(context).exe(lambda: terminate(terminator)))

    try:
        install_signal_handler(loop, lambda: terminate(terminator))
        log().info("CTRL+C to quit")
        loop.run_forever()
    finally:
        log().debug("finally - loop.run_forever()")
