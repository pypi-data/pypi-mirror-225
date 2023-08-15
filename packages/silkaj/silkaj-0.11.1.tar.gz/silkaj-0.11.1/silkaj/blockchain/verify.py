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

import logging
from typing import List
from urllib.error import HTTPError

from click import INT, argument, command, progressbar
from duniterpy.api import bma
from duniterpy.api.client import Client
from duniterpy.documents import Block

from silkaj.constants import BMA_MAX_BLOCKS_CHUNK_SIZE
from silkaj.network import client_instance
from silkaj.tools import message_exit


@command(
    "verify",
    help="Verify blocks’ signatures. \
If only FROM_BLOCK is specified, it verifies from this block to the last block. \
If nothing specified, the whole blockchain gets verified.",
)
@argument("from_block", default=0, type=INT)
@argument("to_block", default=0, type=INT)
def verify_blocks_signatures(from_block: int, to_block: int) -> None:
    client = client_instance()
    to_block = check_passed_blocks_range(client, from_block, to_block)
    invalid_blocks_signatures = []  # type: List[int]
    chunks_from = range(from_block, to_block + 1, BMA_MAX_BLOCKS_CHUNK_SIZE)
    with progressbar(chunks_from, label="Processing blocks verification") as bar:
        for chunk_from in bar:
            chunk_size = get_chunk_size(from_block, to_block, chunks_from, chunk_from)
            logging.info(
                "Processing chunk from block %d to %d",
                chunk_from,
                chunk_from + chunk_size,
            )
            chunk = get_chunk(client, chunk_size, chunk_from)

            for block in chunk:
                block = Block.from_signed_raw(f'{block["raw"]}{block["signature"]}\n')
                verify_block_signature(invalid_blocks_signatures, block)

    display_result(from_block, to_block, invalid_blocks_signatures)


def check_passed_blocks_range(client: Client, from_block: int, to_block: int) -> int:
    head_number = (client(bma.blockchain.current))["number"]
    if to_block == 0:
        to_block = head_number
    if to_block > head_number:
        message_exit(
            f"Passed TO_BLOCK argument is bigger than the head block: {str(head_number)}"
        )
    if from_block > to_block:
        message_exit("TO_BLOCK should be bigger or equal to FROM_BLOCK")
    return to_block


def get_chunk_size(
    from_block: int, to_block: int, chunks_from: range, chunk_from: int
) -> int:
    """If not last chunk, take the maximum size
    Otherwise, calculate the size for the last chunk"""
    if chunk_from != chunks_from[-1]:
        return BMA_MAX_BLOCKS_CHUNK_SIZE
    return (to_block + 1 - from_block) % BMA_MAX_BLOCKS_CHUNK_SIZE


def get_chunk(client: Client, chunk_size: int, chunk_from: int) -> List:
    try:
        chunk = client(bma.blockchain.blocks, chunk_size, chunk_from)
    except HTTPError as e:
        logging.error(e)
        message_exit("Error: Network error to get chunck")
    return chunk


def verify_block_signature(invalid_blocks_signatures: List[int], block: Block) -> None:
    if not block.check_signature(block.issuer):
        invalid_blocks_signatures.append(block.number)


def display_result(
    from_block: int, to_block: int, invalid_blocks_signatures: List[int]
) -> None:
    result = f"Within {from_block}-{to_block} range, "
    if invalid_blocks_signatures:
        result += "blocks with a wrong signature: "
        result += " ".join(str(n) for n in invalid_blocks_signatures)
    else:
        result += "no blocks with a wrong signature."
    print(result)
