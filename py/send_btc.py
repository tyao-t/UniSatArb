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
from bitcoinutils.keys import P2pkhAddress, P2trAddress, PrivateKey, P2wpkhAddress
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('mainnet')
    address = P2wpkhAddress("bc1qtfesujegdagpl5avahjuxq9vjkr36an5389psg")
    print(address.to_script_pub_key())
    # the key that corresponds to the P2WPKH address
    # priv = PrivateKey("cVFkzuEHQKMv6JhkG4hJeL2RqGMmRjkRjk6HutvMVtE356e8UUdf")
    # print(priv.to_bytes())
    # fromAddress = priv.get_public_key().get_segwit_address()
    # print(fromAddress.to_string())
    # print(priv.get_public_key().get_taproot_address().to_string())


#     # UTXO of fromAddress
#     txid = '63202cc09b90cac25b6f60052084a582bdaa61208124f02774b50df55208f7e8'
#     vout = 1

#     # all amounts are needed to sign a taproot input
#     # (depending on sighash)
#     first_amount = to_satoshis(0.000002)
#     amounts = [ first_amount ]

#     # all scriptPubKeys are needed to sign a taproot input 
#     # (depending on sighash) but always of the spend input
#     first_script_pubkey = fromAddress.to_script_pub_key()

#     # alternatively:
#     #first_script_pubkey = Script(['OP_1', pub.to_taproot_hex()])

#     utxos_script_pubkeys = [ first_script_pubkey ]

#     toAddress = P2trAddress('bc1p8eg7s6xf22gr43dkx6v7rhxfz3mj8xrlmsfllw7vxnvwqtsqtzvqfw8205')

#     # create transaction input from tx id of UTXO
#     txin = TxInput(txid, vout)

#     # create transaction output
#     txOut = TxOutput(to_satoshis(0.000002), toAddress.to_script_pub_key())

#     # create transaction without change output - if at least a single input is
#     # segwit we need to set has_segwit=True
#     tx = Transaction([txin], [txOut], has_segwit=True)

#     print("\nRaw transaction:\n" + tx.serialize())

#     print('\ntxid: ' + tx.get_txid())
#     print('\ntxwid: ' + tx.get_wtxid())

#     # sign taproot input
#     # to create the digest message to sign in taproot we need to
#     # pass all the utxos' scriptPubKeys and their amounts
#     sig = priv.sign_taproot_input(tx, 0, utxos_script_pubkeys, \
#                                   amounts)
#     #print(sig)

#     tx.witnesses.append( TxWitnessInput([ sig ]) )

#     # print raw signed transaction ready to be broadcasted
#     print("\nRaw signed transaction:\n" + tx.serialize())

#     print("\nTxId:", tx.get_txid())
#     print("\nTxwId:", tx.get_wtxid())

#     print("\nSize:", tx.get_size())
#     print("\nvSize:", tx.get_vsize())

if __name__ == "__main__":
    main()

