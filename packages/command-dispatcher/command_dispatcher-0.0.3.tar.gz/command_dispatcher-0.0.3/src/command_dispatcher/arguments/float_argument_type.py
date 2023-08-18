from command_dispatcher.arguments.argument_type import ArgumentType
from command_dispatcher.exceptions import ArgumentException


class FloatArgumentType(ArgumentType[float]):
    def parse(self, reader: str) -> float:
        try:
            return float(reader)
        except ValueError:
            raise ArgumentException('argument is not a Number')
