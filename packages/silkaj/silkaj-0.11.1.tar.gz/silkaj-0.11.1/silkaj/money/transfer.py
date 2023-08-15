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


import math
import re
import shlex
import time
from typing import List, Optional, Tuple

import click
from duniterpy.api.bma.tx import process
from duniterpy.documents import (
    BlockID,
    InputSource,
    OutputSource,
    SIGParameter,
    Transaction,
    Unlock,
)
from duniterpy.key import SigningKey

from silkaj import auth, network, public_key, tools, tui
from silkaj.blockchain import tools as bc_tools
from silkaj.constants import (
    BMA_SLEEP,
    CENT_MULT_TO_UNIT,
    MINIMAL_ABSOLUTE_TX_AMOUNT,
    MINIMAL_RELATIVE_TX_AMOUNT,
)
from silkaj.money import tools as m_tools
from silkaj.public_key import gen_pubkey_checksum

MAX_COMMENT_LENGTH = 255


# max size for tx doc is 100 lines.
# Formula for accepted field numbers is:
# (2 * IU + 2 * IS + OUT) <= ( MAX_LINES_IN_TX_DOC - FIX_LINES)
# with IU = inputs/unlocks ; IS = Issuers/Signatures ; OUT = Outpouts.
MAX_LINES_IN_TX_DOC = 100
# 2 lines are necessary, and we block 1 more for the comment
FIX_LINES = 3
# assuming there is only 1 issuer and 2 outputs, max inputs is 46
MAX_INPUTS_PER_TX = 46
# assuming there is 1 issuer and 1 input, max outputs is 93.
MAX_OUTPUTS = 93
# for now, silkaj handles txs for one issuer only
NBR_ISSUERS = 1


@click.command("transfer", help="Transfer money")
@click.option(
    "amounts",
    "--amount",
    "-a",
    multiple=True,
    type=click.FloatRange(MINIMAL_ABSOLUTE_TX_AMOUNT),
    help=f"Quantitative amount(s):\n-a <amount>\nMinimum amount is {MINIMAL_ABSOLUTE_TX_AMOUNT}.",
    cls=tools.MutuallyExclusiveOption,
    mutually_exclusive=["amountsud", "allsources", "file_path"],
)
@click.option(
    "amountsud",
    "--amountUD",
    "-d",
    multiple=True,
    type=click.FloatRange(MINIMAL_RELATIVE_TX_AMOUNT),
    help=f"Relative amount(s):\n-d <amount_UD>\nMinimum amount is {MINIMAL_RELATIVE_TX_AMOUNT}",
    cls=tools.MutuallyExclusiveOption,
    mutually_exclusive=["amounts", "allsources", "file_path"],
)
@click.option(
    "--allSources",
    is_flag=True,
    help="Send all sources to one recipient",
    cls=tools.MutuallyExclusiveOption,
    mutually_exclusive=["amounts", "amountsud", "file_path"],
)
@click.option(
    "recipients",
    "--recipient",
    "-r",
    multiple=True,
    help="Pubkey(s)’ recipients + optional checksum:\n-r <pubkey>[:checksum]\n\
Sending to many recipients is possible:\n\
* With one amount, all will receive the amount\n\
* With many amounts (one per recipient)",
    cls=tools.MutuallyExclusiveOption,
    mutually_exclusive=["file_path"],
)
@click.option(
    "file_path",
    "--file",
    "-f",
    help="File’s path containing a list of amounts in absolute or \
relative reference and recipients’ pubkeys",
    cls=tools.MutuallyExclusiveOption,
    mutually_exclusive=["recipients", "amounts", "amountsUD", "allsources"],
)
@click.option("--comment", "-c", default="", help="Comment")
@click.option(
    "--outputBackChange",
    help="Pubkey recipient to send the rest of the transaction: <pubkey[:checksum]>",
)
@click.option(
    "--yes", "-y", is_flag=True, help="Assume yes. Do not prompt confirmation"
)
def transfer_money(
    amounts: List[float],
    amountsud: List[float],
    allsources: bool,
    recipients: List[str],
    file_path: str,
    comment: str,
    outputbackchange: str,
    yes: bool,
) -> None:
    if file_path:
        tx_amounts, recipients = parse_file_containing_amounts_recipients(file_path)
    else:
        if not (amounts or amountsud or allsources):
            tools.message_exit("Error: amount, amountUD or allSources is not set.")
        if not recipients:
            tools.message_exit("Error: A recipient should be passed")
        if allsources and len(recipients) > 1:
            tools.message_exit(
                "Error: the --allSources option can only be used with one recipient."
            )
        # compute amounts and amountsud
        if not allsources:
            tx_amounts = transaction_amount(amounts, amountsud, recipients)

    key = auth.auth_method()
    issuer_pubkey = key.pubkey

    pubkey_amount = m_tools.get_amount_from_pubkey(issuer_pubkey)
    if allsources:
        if pubkey_amount[0] <= 0:
            tools.message_exit(
                f"Error: Issuer pubkey {gen_pubkey_checksum(issuer_pubkey)} is empty. \
No transaction sent."
            )

        tx_amounts = [pubkey_amount[0]]

    recipients = list(recipients)
    outputbackchange = check_transaction_values(
        comment,
        recipients,
        outputbackchange,
        pubkey_amount[0] < sum(tx_amounts),
        issuer_pubkey,
    )

    if not yes:
        table = tui.Table()
        table.fill_rows(
            gen_confirmation_table(
                issuer_pubkey,
                pubkey_amount[0],
                tx_amounts,
                recipients,
                outputbackchange,
                comment,
            ),
        )
        confirmation_table = table.draw()

    if yes or click.confirm(
        f"{confirmation_table}\nDo you confirm sending this transaction?"
    ):
        handle_intermediaries_transactions(
            key,
            issuer_pubkey,
            tx_amounts,
            recipients,
            comment,
            outputbackchange,
        )


def parse_file_containing_amounts_recipients(
    file_path: str,
) -> Tuple[List[int], List[str]]:
    """
    Parse file in a specific format
    Comments are ignored
    Format should be:
    ```txt
    [ABSOLUTE/RELATIVE]

    # comment1
    amount1 recipient1’s pubkey
    # comment2
    amount2 recipient2’s pubkey
    ```
    """
    reference = ""
    amounts, recipients = [], []
    with open(file_path, encoding="utf-8") as file:
        for n, raw_line in enumerate(file):
            line = shlex.split(raw_line, True)
            if line:
                if n == 0:
                    reference = line[0]
                else:
                    try:
                        amounts.append(float(line[0]))
                        recipients.append(line[1])
                    except (ValueError, IndexError):
                        tools.message_exit(f"Syntax error at line {n + 1}")

    if not reference or reference not in ("ABSOLUTE", "RELATIVE"):
        tools.message_exit(
            f"{file_path} must contain at first line 'ABSOLUTE' or 'RELATIVE' header"
        )

    if not amounts or not recipients:
        tools.message_exit("No amounts or recipients specified")

    # Compute amount depending on the reference
    if reference == "ABSOLUTE":
        reference_mult = CENT_MULT_TO_UNIT
    else:
        reference_mult = m_tools.get_ud_value()
    tx_amounts = compute_amounts(amounts, reference_mult)

    return tx_amounts, recipients


def transaction_amount(
    amounts: List[float], UDs_amounts: List[float], outputAddresses: List[str]
) -> List[int]:
    """
    Check that the number of passed amounts(UD) and recipients are the same
    Returns a list of amounts.
    """
    # Create amounts list
    if amounts:
        amounts_list = compute_amounts(amounts, CENT_MULT_TO_UNIT)
    elif UDs_amounts:
        UD_value = m_tools.get_ud_value()
        amounts_list = compute_amounts(UDs_amounts, UD_value)
    if len(amounts_list) != len(outputAddresses) and len(amounts_list) != 1:
        tools.message_exit(
            "Error: The number of passed recipients is not the same as the passed amounts."
        )
    # In case one amount is passed with multiple recipients
    # generate list containing multiple time the same amount
    if len(amounts_list) == 1 and len(outputAddresses) > 1:
        amounts_list = [amounts_list[0]] * len(outputAddresses)
    return amounts_list


def compute_amounts(amounts: List[float], multiplicator: float) -> List[int]:
    """
    Computes the amounts(UD) and returns a list.
    Multiplicator should be either CENT_MULT_TO_UNIT or UD_Value.
    If relative amount, check that amount is superior to minimal amount.
    """
    # Create amounts list
    amounts_list = []
    for amount in amounts:
        computed_amount = amount * multiplicator
        # check if relative amounts are high enough
        if (multiplicator != CENT_MULT_TO_UNIT) and (
            computed_amount < (MINIMAL_ABSOLUTE_TX_AMOUNT * CENT_MULT_TO_UNIT)
        ):
            tools.message_exit(f"Error: amount {amount} is too low.")
        amounts_list.append(round(computed_amount))
    return amounts_list


def check_transaction_values(
    comment: str,
    outputAddresses: List[str],
    outputBackChange: str,
    enough_source: bool,
    issuer_pubkey: str,
) -> str:
    """
    Check the comment format
    Check the pubkeys and the checksums of the recipients and the outputbackchange
    In case of a valid checksum, assign and return the pubkey without the checksum
    Check the balance is big enough for the transaction
    """
    checkComment(comment)
    # we check output numbers and leave one line for the backchange.
    if len(outputAddresses) > (MAX_OUTPUTS - 1):
        tools.message_exit(
            f"Error : there should be less than {MAX_OUTPUTS - 1} outputs."
        )
    for i, outputAddress in enumerate(outputAddresses):
        if public_key.check_pubkey_format(outputAddress):
            outputAddresses[i] = public_key.validate_checksum(outputAddress)
    if outputBackChange:
        if public_key.check_pubkey_format(outputBackChange):
            outputBackChange = public_key.validate_checksum(outputBackChange)
    if enough_source:
        pubkey = gen_pubkey_checksum(issuer_pubkey)
        tools.message_exit(
            f"{pubkey} pubkey doesn’t have enough money for this transaction."
        )
    return outputBackChange


def gen_confirmation_table(
    issuer_pubkey: str,
    pubkey_amount: int,
    tx_amounts: List[int],
    outputAddresses: List[str],
    outputBackChange: str,
    comment: str,
) -> List[List]:
    """
    Generate transaction confirmation
    """

    currency_symbol = tools.get_currency_symbol()
    ud_value = m_tools.get_ud_value()
    total_tx_amount = sum(tx_amounts)
    tx = []  # type: List[List[str]]
    # display account situation
    m_tools.display_amount(
        tx,
        "Initial balance",
        pubkey_amount,
        ud_value,
        currency_symbol,
    )
    m_tools.display_amount(
        tx,
        "Total transaction amount",
        total_tx_amount,
        ud_value,
        currency_symbol,
    )
    m_tools.display_amount(
        tx,
        "Balance after transaction",
        (pubkey_amount - total_tx_amount),
        ud_value,
        currency_symbol,
    )
    m_tools.display_pubkey(tx, "From", issuer_pubkey)
    # display outputs and amounts
    for outputAddress, tx_amount in zip(outputAddresses, tx_amounts):
        m_tools.display_pubkey(tx, "To", outputAddress)
        time.sleep(BMA_SLEEP)
        m_tools.display_amount(tx, "Amount", tx_amount, ud_value, currency_symbol)
    # display last informations
    if outputBackChange:
        m_tools.display_pubkey(tx, "Backchange", outputBackChange)
    tx.append(["Comment", comment])
    return tx


def get_list_input_for_transaction(
    pubkey: str, TXamount: int, outputs_number: int
) -> Tuple[List[InputSource], int, bool]:
    listinput = m_tools.get_sources(pubkey)[0]
    maxInputsNumber = max_inputs_number(outputs_number, NBR_ISSUERS)
    # generate final list source
    listinputfinal = []
    totalAmountInput = 0
    intermediatetransaction = False
    for nbr_inputs, _input in enumerate(listinput, start=1):
        listinputfinal.append(_input)
        totalAmountInput += m_tools.amount_in_current_base(_input)
        TXamount -= m_tools.amount_in_current_base(_input)
        # if too much sources, it's an intermediate transaction.
        amount_not_reached_and_max_doc_size_reached = (
            TXamount > 0 and MAX_INPUTS_PER_TX <= nbr_inputs
        )
        amount_reached_too_much_inputs = TXamount <= 0 and maxInputsNumber < nbr_inputs
        if (
            amount_not_reached_and_max_doc_size_reached
            or amount_reached_too_much_inputs
        ):
            intermediatetransaction = True
        # if we reach the MAX_INPUTX_PER_TX limit, we send the interm.tx
        # if we gather the good amount, we send the tx :
        #    - either this is no int.tx, and the tx is sent to the receiver,
        #    - or the int.tx it is sent to the issuer before sent to the receiver.
        if MAX_INPUTS_PER_TX <= nbr_inputs or TXamount <= 0:
            break
    if TXamount > 0 and not intermediatetransaction:
        tools.message_exit("Error: you don't have enough money")
    return listinputfinal, totalAmountInput, intermediatetransaction


def handle_intermediaries_transactions(
    key: SigningKey,
    issuers: str,
    tx_amounts: List[int],
    outputAddresses: List[str],
    Comment: str = "",
    OutputbackChange: Optional[str] = None,
) -> None:
    while True:
        # consider there is always one backchange output, hence +1
        listinput_and_amount = get_list_input_for_transaction(
            issuers, sum(tx_amounts), len(outputAddresses) + 1
        )
        intermediatetransaction = listinput_and_amount[2]

        if intermediatetransaction:
            totalAmountInput = listinput_and_amount[1]
            generate_and_send_transaction(
                key,
                issuers,
                [totalAmountInput],
                listinput_and_amount,
                [issuers],
                "Change operation",
            )
        else:
            generate_and_send_transaction(
                key,
                issuers,
                tx_amounts,
                listinput_and_amount,
                outputAddresses,
                Comment,
                OutputbackChange,
            )
            break


def max_inputs_number(outputs_number: int, issuers_number: int) -> int:
    """
    returns the maximum number of inputs.
    This function does not take care of backchange line.
    formula is IU <= (MAX_LINES_IN_TX_DOC - FIX_LINES - O - 2*IS)/2
    """
    return int(
        (MAX_LINES_IN_TX_DOC - FIX_LINES - (2 * issuers_number) - outputs_number) / 2
    )


def generate_and_send_transaction(
    key: SigningKey,
    issuers: str,
    tx_amounts: List[int],
    listinput_and_amount: Tuple[List[InputSource], int, bool],
    outputAddresses: List[str],
    Comment: str,
    OutputbackChange: Optional[str] = None,
) -> None:
    """
    Display sent transaction
    Generate, sign, and send transaction document
    """
    intermediate_tx = listinput_and_amount[2]
    if intermediate_tx:
        print("Generate Change Transaction")
    else:
        print("Generate Transaction:")
    print("   - From:    " + gen_pubkey_checksum(issuers))
    for tx_amount, outputAddress in zip(tx_amounts, outputAddresses):
        display_sent_tx(outputAddress, tx_amount)
    print("   - Total:   " + str(sum(tx_amounts) / 100))

    transaction = generate_transaction_document(
        issuers,
        tx_amounts,
        listinput_and_amount,
        outputAddresses,
        Comment,
        OutputbackChange,
    )
    transaction.sign(key)
    network.send_document(process, transaction)


def display_sent_tx(outputAddress: str, amount: int) -> None:
    print(
        "   - To:     ",
        gen_pubkey_checksum(outputAddress),
        "\n   - Amount: ",
        amount / 100,
    )


def generate_transaction_document(
    issuers: str,
    tx_amounts: List[int],
    listinput_and_amount: Tuple[List[InputSource], int, bool],
    outputAddresses: List[str],
    Comment: str = "",
    OutputbackChange: Optional[str] = None,
) -> Transaction:

    listinput = listinput_and_amount[0]
    totalAmountInput = listinput_and_amount[1]
    total_tx_amount = sum(tx_amounts)

    head_block = bc_tools.get_head_block()

    if not OutputbackChange:
        OutputbackChange = issuers

    # If it's not a foreign exchange transaction,
    # we remove units after two digits after the decimal point
    if issuers not in outputAddresses:
        total_tx_amount = (
            total_tx_amount // 10 ** head_block["unitbase"]
        ) * 10 ** head_block["unitbase"]

    # Generate output
    ################
    listoutput = []  # type: List[OutputSource]
    for tx_amount, outputAddress in zip(tx_amounts, outputAddresses):
        generate_output(listoutput, head_block["unitbase"], tx_amount, outputAddress)

    # Outputs to himself
    rest = totalAmountInput - total_tx_amount
    generate_output(listoutput, head_block["unitbase"], rest, OutputbackChange)

    # Unlocks
    unlocks = generate_unlocks(listinput)

    # Generate transaction document
    ##############################

    return Transaction(
        block_id=BlockID(head_block["number"], head_block["hash"]),
        locktime=0,
        issuers=[issuers],
        inputs=listinput,
        unlocks=unlocks,
        outputs=listoutput,
        comment=Comment,
        currency=head_block["currency"],
    )


def generate_unlocks(listinput: List[InputSource]) -> List[Unlock]:
    unlocks = []
    for i in range(0, len(listinput)):
        unlocks.append(Unlock(index=i, parameters=[SIGParameter(0)]))
    return unlocks


def generate_output(
    listoutput: List[OutputSource], unitbase: int, rest: int, recipient_address: str
) -> None:
    while rest > 0:
        outputAmount = truncBase(rest, unitbase)
        rest -= outputAmount
        if outputAmount > 0:
            outputAmount = int(outputAmount / math.pow(10, unitbase))
            listoutput.append(
                OutputSource(
                    amount=outputAmount,
                    base=unitbase,
                    condition=f"SIG({recipient_address})",
                )
            )
        unitbase = unitbase - 1


def checkComment(comment: str) -> None:
    if len(comment) > MAX_COMMENT_LENGTH:
        tools.message_exit("Error: Comment is too long")
    regex = re.compile(
        "^[0-9a-zA-Z\\ \\-\\_\\:\\/\\;\\*\\[\\]\\(\\)\\?\
\\!\\^\\+\\=\\@\\&\\~\\#\\{\\}\\|\\\\<\\>\\%\\.]*$"
    )
    if not re.search(regex, comment):
        tools.message_exit("Error: the format of the comment is invalid")


def truncBase(amount: int, base: int) -> int:
    _pow = int(math.pow(10, base))
    if amount < _pow:
        return 0
    return math.trunc(amount / _pow) * _pow
