# Copyright  2016-2022 Maël Azimi <m.a@moul.re>
#
# Silkaj is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Silkaj is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Silkaj. If not, see <https://www.gnu.org/licenses/>.

import functools
import sys
from typing import Any

import click

from silkaj.blockchain.tools import get_blockchain_parameters
from silkaj.constants import FAILURE_EXIT_STATUS, G1_SYMBOL, GTEST_SYMBOL


@functools.lru_cache(maxsize=1)
def get_currency_symbol() -> str:
    params = get_blockchain_parameters()
    if params["currency"] == "g1":
        return G1_SYMBOL
    return GTEST_SYMBOL


def message_exit(message: str) -> None:
    print(message)
    sys.exit(FAILURE_EXIT_STATUS)


# pylint: disable=too-few-public-methods
class MutuallyExclusiveOption(click.Option):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        self.mutually_exclusive = set(kwargs.pop("mutually_exclusive", []))
        _help = kwargs.get("help", "")
        if self.mutually_exclusive:
            ex_str = ", ".join(self.mutually_exclusive)
            kwargs[
                "help"
            ] = f"{_help} NOTE: This argument is mutually exclusive with arguments: [{ex_str}]."
        super().__init__(*args, **kwargs)

    def handle_parse_result(self, ctx: click.Context, opts: Any, args: Any) -> Any:
        if self.mutually_exclusive.intersection(opts) and self.name in opts:
            arguments = ", ".join(self.mutually_exclusive)
            raise click.UsageError(
                f"Usage: `{self.name}` is mutually exclusive with arguments `{arguments}`."
            )

        return super().handle_parse_result(ctx, opts, args)
