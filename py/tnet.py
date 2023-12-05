# Copyright (C) 2018-2023 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.

from binascii import hexlify
from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import P2pkhAddress, P2trAddress, PrivateKey
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('testnet')

    privA = PrivateKey("cUrtpHMVj73rbzBHWfJvv29cP9XUBmBzPXcUg8H8ZJiZhDEZNaxx")
    privB = PrivateKey("cVFkzuEHQKMv6JhkG4hJeL2RqGMmRjkRjk6HutvMVtE356e8UUdf")
    # print(priv.to_wif())
    pubA = privA.get_public_key()
    pubB = privB.get_public_key()

    addressA = pubA.get_taproot_address()
    addressB = pubB.get_taproot_address()
    print(addressA.to_string())
    print(addressB.to_string())

    
    
    script_pubkeyA = addressA.to_script_pub_key()
    script_pubkeyB = addressB.to_script_pub_key()
    utxos_script_pubkeys = [script_pubkeyA]

    txin1 = TxInput("d94ebbb47926ae986128652d6df9af4d108e95849bf8741b66de3692cd3ca1ef", 0)
    txin2 = TxInput("796a7a74f20f29a7c13bdfe3e3cafa5205842a98800836b7a54a5e0c36c55e93", 1)

    amounts = [to_satoshis(0.000001)]
    txOut = TxOutput(to_satoshis(0.000001), addressB.to_script_pub_key())
    tx = Transaction([txin1], [txOut], has_segwit=True)
    sig1 = privA.sign_taproot_input(tx, 0, utxos_script_pubkeys, amounts)
    tx.witnesses.append( TxWitnessInput([sig1]) )

    print("\nRaw signed transaction:\n" + tx.serialize())

if __name__ == "__main__":
    main()

