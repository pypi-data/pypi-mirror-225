"""Simple app."""
import click
from click_groups import GroupedGroup


@click.group(cls=GroupedGroup)
def cli():
    """Run commands."""
    pass


@cli.command(help_group="Group 1", priority=10)
def command_1():
    """Run a command."""


@cli.command(help_group="Group 1")
def command_2():
    """Run a command."""


@cli.command(help_group="Group 2")
def command_3():
    """Run a command."""


@cli.command(help_group="Group 3")
def command_4():
    """Run a command."""


@cli.command()
def command_5():
    """Run a command."""


@click.group(cls=GroupedGroup)
def command_6():
    """Run a command."""


cli.add_command(command_6)


@click.group(cls=GroupedGroup)
def command_7():
    """Run a command."""


cli.add_command(command_7, help_group="Group 1", priority=0)

if __name__ == "__main__":
    cli()
