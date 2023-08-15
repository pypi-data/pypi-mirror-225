"""Click extensions."""

from collections import OrderedDict
from typing import Any, Dict, List, Optional

import click


class OrderedGroup(click.Group):
    """Group preserving the order of subcommands."""

    # See:
    # https://github.com/pallets/click/issues/513#issuecomment-504158316
    # https://stackoverflow.com/a/58323807

    def __init__(
        self,
        name: Optional[str] = None,
        commands: Optional[Dict[str, click.Command]] = None,
        **attrs: Dict[str, Any],
    ) -> None:
        """Construct a group."""
        if commands is None:
            commands = OrderedDict()
        elif not isinstance(commands, OrderedDict):
            commands = OrderedDict(commands)
        super(OrderedGroup, self).__init__(name=name, commands=commands, **attrs)

    def list_commands(self, ctx: click.Context) -> List[str]:
        """Return a list of subcommands in the order they should appear."""
        return list(self.commands.keys())
