from command_dispatcher.arguments.argument_type import ArgumentType
from command_dispatcher.exceptions import ArgumentException


class BoolArgumentType(ArgumentType[bool]):
    def parse(self, reader: str) -> bool:
        if reader in ['True', 'true', 'T', 't', 'Yes', 'yes', 'Y', 'y']:
            return True
        elif reader in ['False', 'false', 'F', 'f', 'No', 'no', 'N', 'n']:
            return False
        else:
            raise ArgumentException('argument is not a Boolean')
