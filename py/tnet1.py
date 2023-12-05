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
from bitcoinutils.constants import SIGHASH_ALL, SIGHASH_SINGLE, SIGHASH_NONE, SIGHASH_ANYONECANPAY
from bitcoinutils.keys import P2pkhAddress, PrivateKey
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('testnet')

    # the key that corresponds to the P2WPKH address
    priv = PrivateKey("cUrtpHMVj73rbzBHWfJvv29cP9XUBmBzPXcUg8H8ZJiZhDEZNaxx")

    pub = priv.get_public_key()

    fromAddress = pub.get_taproot_address()
    print(fromAddress.to_string())

    # UTXO of fromAddress
    txid = '796a7a74f20f29a7c13bdfe3e3cafa5205842a98800836b7a54a5e0c36c55e93'
    vout = 1

    # all amounts are needed to sign a taproot input
    # (depending on sighash)
    first_amount = to_satoshis(0.00005)
    amounts = [ first_amount ]

    # all scriptPubKeys are needed to sign a taproot input 
    # (depending on sighash) but always of the spend input
    # first_script_pubkey = fromAddress.to_script_pub_key()

    # alternatively:
    first_script_pubkey = Script(['OP_1', pub.to_taproot_hex()])

    utxos_script_pubkeys = [ first_script_pubkey ]

    toAddress = P2pkhAddress('mtVHHCqCECGwiMbMoZe8ayhJHuTdDbYWdJ')

    # create transaction input from tx id of UTXO
    txin = TxInput(txid, vout)

    # create transaction output
    txOut = TxOutput(to_satoshis(0.00004), toAddress.to_script_pub_key())

    # create transaction without change output - if at least a single input is
    # segwit we need to set has_segwit=True
    tx = Transaction([txin], [txOut], has_segwit=True)

    print("\nRaw transaction:\n" + tx.serialize())

    print('\ntxid: ' + tx.get_txid())
    print('\ntxwid: ' + tx.get_wtxid())

    # sign taproot input
    # to create the digest message to sign in taproot we need to
    # pass all the utxos' scriptPubKeys and their amounts
    sig = priv.sign_taproot_input(tx, 0, utxos_script_pubkeys, \
                                  amounts, sighash=SIGHASH_SINGLE)
    #print(sig)

    tx.witnesses.append( TxWitnessInput([ sig]) )

    # print raw signed transaction ready to be broadcasted
    print("\nRaw signed transaction:\n" + tx.serialize())

    print("\nTxId:", tx.get_txid())
    print("\nTxwId:", tx.get_wtxid())

    print("\nSize:", tx.get_size())
    print("\nvSize:", tx.get_vsize())

if __name__ == "__main__":
    main()