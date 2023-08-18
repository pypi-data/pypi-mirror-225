from typing import Callable, Coroutine, Any

from command_dispatcher.command_source import S
from command_dispatcher.command_context import CommandContext

Command = Callable[[CommandContext[S]], Coroutine[Any, Any, Any]]
