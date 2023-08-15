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

from collections import OrderedDict
from operator import itemgetter
from os import system
from typing import Dict, Tuple

import click
import jsonschema
from duniterpy.api import bma
from duniterpy.api.client import WSConnection
from pendulum import from_timestamp
from websocket._exceptions import WebSocketConnectionClosedException

from silkaj import network, tui
from silkaj.constants import ALL


@click.command(
    "difficulty",
    help="Display the current Proof of Work difficulty level to generate the next block",
)
def difficulties() -> None:
    client = network.client_instance()
    try:
        ws = client(bma.ws.block)
        while True:
            current = ws.receive_json()
            jsonschema.validate(current, bma.ws.WS_BLOCK_SCHEMA)
            diffi = client(bma.blockchain.difficulties)
            display_diffi(current, diffi)
    except (jsonschema.ValidationError, WebSocketConnectionClosedException) as e:
        print(f"{str(e.__class__.__name__)}: {str(e)}")


def display_diffi(current: WSConnection, diffi: Dict) -> None:
    levels = [OrderedDict((i, d[i]) for i in ("uid", "level")) for d in diffi["levels"]]
    diffi["levels"] = levels
    issuers = 0
    sorted_diffi = sorted(diffi["levels"], key=itemgetter("level"), reverse=True)
    for d in diffi["levels"]:
        if d["level"] / 2 < current["powMin"]:
            issuers += 1
        d["match"] = match_pattern(d["level"])[0][:20]
        d["Π diffi"] = compute_power(match_pattern(d["level"])[1])
        d["Σ diffi"] = d.pop("level")
    system("cls||clear")
    block_gen = from_timestamp(current["time"], tz="local").format(ALL)
    match = match_pattern(int(current["powMin"]))[0]

    table = tui.Table(style="columns").set_cols_dtype(["t", "t", "t", "i"])
    table.fill_from_dict_list(sorted_diffi)

    content = f'Current block: n°{current["number"]}, generated on {block_gen}\n\
Generation of next block n°{diffi["block"]} \
possible by at least {issuers}/{len(diffi["levels"])} members\n\
Common Proof-of-Work difficulty level: {current["powMin"]}, hash starting with `{match}`\n\
{table.draw()}'
    print(content)


def match_pattern(_pow: int, match: str = "", p: int = 1) -> Tuple[str, int]:
    while _pow > 0:
        if _pow >= 16:
            match += "0"
            _pow -= 16
            p *= 16
        else:
            match += f"[0-{hex(15 - _pow)[2:].upper()}]"
            p *= _pow
            _pow = 0
    return f"{match}*", p


def compute_power(nbr: float, power: int = 0) -> str:
    while nbr >= 10:
        nbr /= 10
        power += 1
    return f"{nbr:.1f} × 10^{power}"
