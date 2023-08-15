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

import sys

from click import Context, group, help_option, option, pass_context, version_option
from duniterpy.api.endpoint import endpoint as du_endpoint

from silkaj.about import about
from silkaj.auth import generate_auth_file
from silkaj.blockchain.blocks import list_blocks
from silkaj.blockchain.difficulty import difficulties
from silkaj.blockchain.information import currency_info
from silkaj.blockchain.verify import verify_blocks_signatures
from silkaj.checksum import checksum_command
from silkaj.constants import (
    G1_DEFAULT_ENDPOINT,
    G1_TEST_DEFAULT_ENDPOINT,
    SILKAJ_VERSION,
)
from silkaj.g1_monetary_license import license_command
from silkaj.money.balance import balance_cmd
from silkaj.money.history import transaction_history
from silkaj.money.transfer import transfer_money
from silkaj.wot import revocation
from silkaj.wot.certification import certify
from silkaj.wot.lookup import lookup_cmd
from silkaj.wot.membership import send_membership
from silkaj.wot.status import status


@group()
@help_option("-h", "--help")
@version_option(SILKAJ_VERSION, "-v", "--version")
@option(
    "--endpoint",
    "-ep",
    help=f"Default endpoint to reach Ğ1 currency by its official node\
 {du_endpoint(G1_DEFAULT_ENDPOINT).host}\
 This option allows to specify a custom endpoint as follow: <host>:<port>.\
 In case no port is specified, it defaults to 443.",
)
@option(
    "--gtest",
    "-gt",
    is_flag=True,
    help=f"Default endpoint to reach ĞTest currency by its official node: \
{du_endpoint(G1_TEST_DEFAULT_ENDPOINT).host}",
)
@option(
    "--auth-scrypt",
    "--scrypt",
    is_flag=True,
    help="Scrypt authentication: default method",
)
@option("--nrp", help='Scrypt parameters: defaults N,r,p: "4096,16,1"')
@option(
    "--auth-file",
    "-af",
    is_flag=True,
    help="Authentication file. Defaults to: './authfile'",
)
@option(
    "--file",
    default="authfile",
    show_default=True,
    help="Path file specification with '--auth-file'",
)
@option("--auth-seed", "--seed", is_flag=True, help="Seed hexadecimal authentication")
@option("--auth-wif", "--wif", is_flag=True, help="WIF and EWIF authentication methods")
@option(
    "--display",
    "-d",
    is_flag=True,
    help="Display the generated document before sending it",
)
@option(
    "--dry-run",
    "-n",
    is_flag=True,
    help="By-pass licence, confirmation. \
Do not send the document, but display it instead",
)
@pass_context
def cli(
    ctx: Context,
    endpoint: str,
    gtest: bool,
    auth_scrypt: bool,
    nrp: str,
    auth_file: bool,
    file: str,
    auth_seed: bool,
    auth_wif: bool,
    display: bool,
    dry_run: bool,
) -> None:
    if display and dry_run:
        sys.exit("ERROR: display and dry-run options can not be used together")

    ctx.obj = {}
    ctx.ensure_object(dict)
    ctx.obj["ENDPOINT"] = endpoint
    ctx.obj["GTEST"] = gtest
    ctx.obj["AUTH_SCRYPT"] = auth_scrypt
    ctx.obj["AUTH_SCRYPT_PARAMS"] = nrp
    ctx.obj["AUTH_FILE"] = auth_file
    ctx.obj["AUTH_FILE_PATH"] = file
    ctx.obj["AUTH_SEED"] = auth_seed
    ctx.obj["AUTH_WIF"] = auth_wif
    ctx.obj["DISPLAY_DOCUMENT"] = display
    ctx.obj["DRY_RUN"] = dry_run


cli.add_command(about)
cli.add_command(generate_auth_file)
cli.add_command(checksum_command)
cli.add_command(license_command)


@cli.group("blockchain", help="Blockchain related commands")
@help_option("-h", "--help")
def blockchain_group() -> None:
    pass


blockchain_group.add_command(list_blocks)
blockchain_group.add_command(difficulties)
blockchain_group.add_command(currency_info)
blockchain_group.add_command(verify_blocks_signatures)


@cli.group("money", help="Money management related commands")
@help_option("-h", "--help")
def money_group() -> None:
    pass


money_group.add_command(balance_cmd)
money_group.add_command(transaction_history)
money_group.add_command(transfer_money)


@cli.group("wot", help="Web-of-Trust related commands")
@help_option("-h", "--help")
def wot_group() -> None:
    pass


wot_group.add_command(certify)
wot_group.add_command(lookup_cmd)
wot_group.add_command(send_membership)
wot_group.add_command(status)


@wot_group.group(
    "revocation",
    help="Create, save, verify or publish revocation document.\n\
Subcommands optionally take the path to the revocation document.",
)
@help_option("-h", "--help")
def revocation_group() -> None:
    pass


revocation_group.add_command(revocation.create)
revocation_group.add_command(revocation.verify)
revocation_group.add_command(revocation.publish)
revocation_group.add_command(revocation.revoke_now)
