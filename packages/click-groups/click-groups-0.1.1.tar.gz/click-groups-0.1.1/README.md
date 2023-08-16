# click-groups

[![License](https://img.shields.io/pypi/l/click-groups.svg?color=green)](https://github.com/lukasz-migas/click-groups/raw/main/LICENSE)
[![PyPI](https://img.shields.io/pypi/v/click-groups.svg?color=green)](https://pypi.org/project/click-groups)
[![Python Version](https://img.shields.io/pypi/pyversions/click-groups.svg?color=green)](https://python.org)
[![CI](https://github.com/lukasz-migas/click-groups/actions/workflows/ci.yml/badge.svg)](https://github.com/lukasz-migas/click-groups/actions/workflows/ci.yml)
[![codecov](https://codecov.io/gh/lukasz-migas/click-groups/branch/main/graph/badge.svg)](https://codecov.io/gh/lukasz-migas/click-groups)

Enable grouping and ordering of commands.

Would you like to split your commands into sub-groups so that they are nicely organized? Or perhaps you would like to ensure that the order of your commands stays consistent?

Now you can do this by specifying few additional group attributes.

In your [click](http://click.pocoo.org/) app:

```python
import click
from click_groups import GroupedGroup

@click.group(cls=GroupedGroup)
def cli():
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
```

Which will result in:
```
Usage: cli [OPTIONS] COMMAND [ARGS]...

Options:
  --help  Show this message and exit.

Group 1:
  command-7  Run a command.
  command-2  Run a command.
  command-1  Run a command.

Group 2:
  command-3  Run a command.

Group 3:
  command-4  Run a command.

Commands:
  command-5  Run a command.
  command-6  Run a command.
```

## Contributing

Contributions are always welcome. Please feel free to submit PRs with new features, bug fixes, or documentation improvements.

```bash
git clone https://github.com/lukasz-migas/click-groups.git

pip install -e .[dev]
```