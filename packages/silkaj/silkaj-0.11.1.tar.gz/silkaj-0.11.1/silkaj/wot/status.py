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
from typing import Dict, List, Tuple

import click
from duniterpy.api.bma import blockchain, wot
from pendulum import from_timestamp, now

from silkaj.blockchain.tools import get_blockchain_parameters
from silkaj.constants import DATE
from silkaj.network import client_instance
from silkaj.public_key import gen_pubkey_checksum, is_pubkey_and_check
from silkaj.tui import Table
from silkaj.wot import tools as wt


def get_sent_certifications(
    signed: List, time_first_block: int, params: Dict
) -> Tuple[List[str], List[str]]:
    sent = []
    expire = []
    if signed:
        for cert in signed:
            sent.append(cert["uid"])
            expire.append(
                expiration_date_from_block_id(
                    cert["cert_time"]["block"], time_first_block, params
                )
            )
    return sent, expire


@click.command(
    "status",
    help="Check received and sent certifications and \
consult the membership status of any given identity",
)
@click.argument("uid_pubkey")
def status(uid_pubkey: str) -> None:
    """
    get searched id
    get id of received and sent certifications
    display in a table the result with the numbers
    """
    client = client_instance()
    first_block = client(blockchain.block, 1)
    time_first_block = first_block["time"]

    checked_pubkey = is_pubkey_and_check(uid_pubkey)
    if checked_pubkey:
        uid_pubkey = str(checked_pubkey)

    identity, pubkey, signed = wt.choose_identity(uid_pubkey)
    certifications = OrderedDict()  # type: OrderedDict
    params = get_blockchain_parameters()

    req = None
    requirements = client(wot.requirements, pubkey)
    for req in requirements["identities"]:
        if req["pubkey"] == pubkey:
            break

    certifications["received_expire"] = []
    certifications["received"] = []
    certifications["sent"] = []
    certifications["sent_expire"] = []
    for cert in identity["others"]:
        certifications["received_expire"].append(
            expiration_date_from_block_id(
                cert["meta"]["block_number"], time_first_block, params
            )
        )
        certifications["received"].append(
            cert_written_in_the_blockchain(req["certifications"], cert)
        )
        (
            certifications["sent"],
            certifications["sent_expire"],
        ) = get_sent_certifications(signed, time_first_block, params)
    nbr_sent_certs = len(certifications["sent"]) if "sent" in certifications else 0

    table = Table(style="columns").set_cols_align(["r", "r", "r", "r"])
    table.fill_from_dict(certifications)

    print(
        f'{identity["uid"]} ({gen_pubkey_checksum(pubkey, True)}) \
from block #{identity["meta"]["timestamp"][:15]}…\n\
received {len(certifications["received"])} and sent \
{nbr_sent_certs}/{params["sigStock"]} certifications:\n\
{table.draw()}\n\
✔: Certification available to be written or already written into the blockchain\n'
    )
    membership_status(certifications, pubkey, req)


def cert_written_in_the_blockchain(written_certs: Dict, certifieur: Dict):
    for cert in written_certs:
        if cert["from"] == certifieur["pubkey"]:
            return certifieur["uids"][0] + " ✔"
    return certifieur["uids"][0]


def membership_status(certifications: OrderedDict, pubkey: str, req: Dict) -> None:
    params = get_blockchain_parameters()
    if len(certifications["received"]) >= params["sigQty"]:
        date = certifications["received_expire"][
            len(certifications["received"]) - params["sigQty"]
        ]
        print(f"Membership expiration due to certification expirations: {date}")
    member_lookup = wt.is_member(pubkey)
    is_member = bool(member_lookup)
    print("member:", is_member)
    if req["revoked"]:
        revoke_date = from_timestamp(req["revoked_on"], tz="local").format(DATE)
        print(f"revoked: {req['revoked']}\nrevoked on: {revoke_date}")
    if not is_member and req["wasMember"]:
        print("expired:", req["expired"], "\nwasMember:", req["wasMember"])
    elif is_member:
        expiration_date = now().add(seconds=req["membershipExpiresIn"]).format(DATE)
        print(f"Membership document expiration: {expiration_date}")
        print("Sentry:", req["isSentry"])
    print("outdistanced:", req["outdistanced"])


def expiration_date_from_block_id(
    block_id: str, time_first_block: int, params: Dict
) -> str:
    expir_timestamp = (
        date_approximation(block_id, time_first_block, params["avgGenTime"])
        + params["sigValidity"]
    )
    return from_timestamp(expir_timestamp, tz="local").format(DATE)


def date_approximation(block_id, time_first_block, avgentime):
    return time_first_block + block_id * avgentime
