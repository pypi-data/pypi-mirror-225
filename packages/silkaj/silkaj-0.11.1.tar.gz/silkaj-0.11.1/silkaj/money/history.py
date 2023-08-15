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

from operator import eq, itemgetter, ne, neg
from typing import Any, List, Optional, Tuple
from urllib.error import HTTPError

from click import argument, command, echo_via_pager, option
from duniterpy.api.bma.tx import history
from duniterpy.api.client import Client
from duniterpy.documents.transaction import OutputSource, Transaction
from duniterpy.grammars.output import Condition
from pendulum import from_timestamp, now

from silkaj.constants import ALL, ALL_DIGITAL
from silkaj.money.tools import (
    amount_in_current_base,
    get_amount_from_pubkey,
    get_ud_value,
)
from silkaj.network import client_instance
from silkaj.public_key import (
    check_pubkey_format,
    gen_pubkey_checksum,
    validate_checksum,
)
from silkaj.tools import get_currency_symbol
from silkaj.tui import Table
from silkaj.wot import tools as wt


@command("history", help="Display transaction history")
@argument("pubkey")
@option("--uids", "-u", is_flag=True, help="Display uids")
@option("--full-pubkey", "-f", is_flag=True, help="Display full-length pubkeys")
def transaction_history(pubkey: str, uids: bool, full_pubkey: bool) -> None:
    if check_pubkey_format(pubkey):
        pubkey = validate_checksum(pubkey)

    client = client_instance()
    ud_value = get_ud_value()
    currency_symbol = get_currency_symbol()

    header = generate_header(pubkey, currency_symbol, ud_value)
    received_txs, sent_txs = [], []  # type: List[Transaction], List[Transaction]
    get_transactions_history(client, pubkey, received_txs, sent_txs)
    remove_duplicate_txs(received_txs, sent_txs)

    txs_list = generate_txs_list(
        received_txs, sent_txs, pubkey, ud_value, currency_symbol, uids, full_pubkey
    )
    table_headers = [
        "Date",
        "Issuers/Recipients",
        f"Amounts {currency_symbol}",
        f"Amounts UD{currency_symbol}",
        "Comment",
    ]
    table = Table()
    table.fill_rows(txs_list, table_headers)
    echo_via_pager(header + table.draw())


def generate_header(pubkey: str, currency_symbol: str, ud_value: int) -> str:
    try:
        idty = wt.identity_of(pubkey)
    except HTTPError:
        idty = dict([("uid", "")])
    balance = get_amount_from_pubkey(pubkey)
    balance_ud = round(balance[1] / ud_value, 2)
    date = now().format(ALL)
    return f'Transactions history from: {idty["uid"]} {gen_pubkey_checksum(pubkey)}\n\
Current balance: {balance[1] / 100} {currency_symbol}, {balance_ud} UD {currency_symbol} on {date}\n'


def get_transactions_history(
    client: Client, pubkey: str, received_txs: List, sent_txs: List
) -> None:
    """
    Get transaction history
    Store txs in Transaction object
    """
    tx_history = client(history, pubkey)
    currency = tx_history["currency"]

    for received in tx_history["history"]["received"]:
        received_txs.append(Transaction.from_bma_history(received, currency))
    for sent in tx_history["history"]["sent"]:
        sent_txs.append(Transaction.from_bma_history(sent, currency))


def remove_duplicate_txs(received_txs: List, sent_txs: List) -> None:
    """
    Remove duplicate transactions from history
    Remove received tx which contains output back return
    that we don’t want to displayed
    A copy of received_txs is necessary to remove elements
    """
    for received_tx in list(received_txs):
        if received_tx in sent_txs:
            received_txs.remove(received_tx)


def generate_txs_list(
    received_txs: List[Transaction],
    sent_txs: List[Transaction],
    pubkey: str,
    ud_value: int,
    currency_symbol: str,
    uids: bool,
    full_pubkey: bool,
) -> List:
    """
    Generate information in a list of lists for texttable
    Merge received and sent txs
    Sort txs temporarily
    """

    received_txs_list, sent_txs_list = (
        [],
        [],
    )  # type: List[Transaction], List[Transaction]
    parse_received_tx(
        received_txs_list, received_txs, pubkey, ud_value, uids, full_pubkey
    )
    parse_sent_tx(sent_txs_list, sent_txs, pubkey, ud_value, uids, full_pubkey)
    txs_list = received_txs_list + sent_txs_list

    txs_list.sort(key=itemgetter(0), reverse=True)
    return txs_list


def parse_received_tx(
    received_txs_table: List[Transaction],
    received_txs: List[Transaction],
    pubkey: str,
    ud_value: int,
    uids: bool,
    full_pubkey: bool,
) -> None:
    """
    Extract issuers’ pubkeys
    Get identities from pubkeys
    Convert time into human format
    Assign identities
    Get amounts and assign amounts and amounts_ud
    Append comment
    """
    issuers = []
    for received_tx in received_txs:
        for issuer in received_tx.issuers:
            issuers.append(issuer)
    identities = wt.identities_from_pubkeys(issuers, uids)
    for received_tx in received_txs:
        tx_list = []
        tx_list.append(from_timestamp(received_tx.time, tz="local").format(ALL_DIGITAL))
        tx_list.append("")
        for i, issuer in enumerate(received_tx.issuers):
            tx_list[1] += prefix(None, None, i) + assign_idty_from_pubkey(
                issuer, identities, full_pubkey
            )
        amounts = tx_amount(received_tx, pubkey, received_func)[0]
        tx_list.append(amounts / 100)
        tx_list.append(amounts / ud_value)
        tx_list.append(received_tx.comment)
        received_txs_table.append(tx_list)


def parse_sent_tx(
    sent_txs_table: List[Transaction],
    sent_txs: List[Transaction],
    pubkey: str,
    ud_value: int,
    uids: bool,
    full_pubkey: bool,
) -> None:
    # pylint: disable=too-many-locals
    """
    Extract recipients’ pubkeys from outputs
    Get identities from pubkeys
    Convert time into human format
    Store "Total" and total amounts according to the number of outputs
    If not output back return:
    Assign amounts, amounts_ud, identities, and comment
    """
    pubkeys = []
    for sent_tx in sent_txs:
        outputs = tx_amount(sent_tx, pubkey, sent_func)[1]
        for output in outputs:
            if output_available(output.condition, ne, pubkey):
                pubkeys.append(output.condition.left.pubkey)

    identities = wt.identities_from_pubkeys(pubkeys, uids)
    for sent_tx in sent_txs:
        tx_list = []
        tx_list.append(from_timestamp(sent_tx.time, tz="local").format(ALL_DIGITAL))

        total_amount, outputs = tx_amount(sent_tx, pubkey, sent_func)
        if len(outputs) > 1:
            tx_list.append("Total")
            amounts = str(total_amount / 100)
            amounts_ud = str(round(total_amount / ud_value, 2))
        else:
            tx_list.append("")
            amounts = ""
            amounts_ud = ""

        for i, output in enumerate(outputs):
            if output_available(output.condition, ne, pubkey):
                amounts += prefix(None, outputs, i) + str(
                    neg(amount_in_current_base(output)) / 100
                )
                amounts_ud += prefix(None, outputs, i) + str(
                    round(neg(amount_in_current_base(output)) / ud_value, 2)
                )
                tx_list[1] += prefix(tx_list[1], outputs, 0) + assign_idty_from_pubkey(
                    output.condition.left.pubkey, identities, full_pubkey
                )
        tx_list.append(amounts)
        tx_list.append(amounts_ud)
        tx_list.append(sent_tx.comment)
        sent_txs_table.append(tx_list)


def tx_amount(
    tx: List[Transaction], pubkey: str, function: Any
) -> Tuple[int, List[OutputSource]]:
    """
    Determine transaction amount from output sources
    """
    amount = 0
    outputs = []
    for output in tx.outputs:  # type: ignore
        if output_available(output.condition, ne, pubkey):
            outputs.append(output)
        amount += function(output, pubkey)
    return amount, outputs


def received_func(output: OutputSource, pubkey: str) -> int:
    if output_available(output.condition, eq, pubkey):
        return amount_in_current_base(output)
    return 0


def sent_func(output: OutputSource, pubkey: str) -> int:
    if output_available(output.condition, ne, pubkey):
        return neg(amount_in_current_base(output))
    return 0


def output_available(condition: Condition, comparison: Any, value: str) -> bool:
    """
    Check if output source is available
    Currently only handle simple SIG condition
    XHX, CLTV, CSV should be handled when present in the blockchain
    """
    if hasattr(condition.left, "pubkey"):
        return comparison(condition.left.pubkey, value)
    return False


def assign_idty_from_pubkey(pubkey: str, identities: List, full_pubkey: bool) -> str:
    idty = gen_pubkey_checksum(pubkey, short=not full_pubkey)
    for identity in identities:
        if pubkey == identity["pubkey"]:
            pubkey_mod = gen_pubkey_checksum(pubkey, short=not full_pubkey)
            idty = f'{identity["uid"]} - {pubkey_mod}'
    return idty


def prefix(
    tx_addresses: Optional[str], outputs: Optional[List[OutputSource]], occurence: int
) -> str:
    """
    Pretty print with texttable
    Break line when several values in a cell

    Received tx case, 'outputs' is not defined, then add a breakline
    between the pubkeys except for the first occurence for multi-sig support

    Sent tx case, handle "Total" line in case of multi-output txs
    In case of multiple outputs, there is a "Total" on the top,
    where there must be a breakline
    """

    if not outputs:
        return "\n" if occurence > 0 else ""

    if tx_addresses == "Total":
        return "\n"
    return "\n" if len(outputs) > 1 else ""
