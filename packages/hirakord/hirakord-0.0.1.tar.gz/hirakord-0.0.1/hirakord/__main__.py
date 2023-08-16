"""
MIT License

Copyright (c) 2023 Andrew (ExHiraku) M

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import click
import os
import pkg_resources
from typing import Dict, List, Optional


HELPER_DEPENDENCIES: Dict[str, List[str]] = {"cog": ["logger"]}


def ensure_dependencies(name: str) -> bool:
    return all(os.path.isfile(f"helpers/{dep}.py") for dep in HELPER_DEPENDENCIES.get(name, []))


def get_helper(helper_name: str) -> Optional[str]:
    try:
        content = pkg_resources.resource_string('hirakord', f'templates/helpers/{helper_name}.txt')
        if not ensure_dependencies(helper_name):
            missing_deps = ", ".join(HELPER_DEPENDENCIES[helper_name])
            click.echo(f"Missing dependencies: {missing_deps}. Install them first.")
            return None
        return content.decode('utf-8').replace('\r\n', '\n')
    except FileNotFoundError:
        print(f"Helper {helper_name} does not exist.")
        return None


@click.group()
def cli() -> None:
    """Hirakord Discord bot helper"""
    pass


@cli.group()
def helper() -> None:
    """Commands for helpers."""
    pass


@helper.command()
@click.argument('name')
def add(name: str) -> None:
    """Add a specified helper."""
    # Create a helpers directory if not exists
    if not os.path.exists("helpers"):
        os.makedirs("helpers")

    helper = get_helper(name)
    if not helper:
        return

    with open(f"helpers/{name}.py", "w") as f:
        f.write(helper)

    click.echo(f'{name.title()} helper added successfully!')


if __name__ == '__main__':
    cli()
