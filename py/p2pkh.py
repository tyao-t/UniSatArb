# Copyright (C) 2018-2022 The python-bitcoin-utils developers
#
# This file is part of python-bitcoin-utils
#
# It is subject to the license terms in the LICENSE file found in the top-level
# directory of this distribution.
#
# No part of python-bitcoin-utils, including this file, may be copied,
# modified, propagated, or distributed except according to the terms contained
# in the LICENSE file.


from bitcoinutils.setup import setup
from bitcoinutils.utils import to_satoshis
from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
from bitcoinutils.keys import P2pkhAddress, P2trAddress, PrivateKey, P2wpkhAddress
from bitcoinutils.script import Script

def main():
    # always remember to setup the network
    setup('testnet')

    # create transaction input from tx id of UTXO (contained 0.4 tBTC)
    txin = TxInput('ee9c24e8cf2fb940aa72bd3307da6d500049e3bfbc640c40f0ff26f2c0cb8da0', 1)

    # sk = PrivateKey('cUrtpHMVj73rbzBHWfJvv29cP9XUBmBzPXcUg8H8ZJiZhDEZNaxx')
    # sk = PrivateKey()
    priv = PrivateKey("cRUGeuFL552ty3WcmgyNxvmJgufQuuRqGXNx65h5Bh9tvd2xx74P")
    from_addr = P2wpkhAddress("tb1q026q3uact4p062cq95057mme43h462sn2cpkes")
    # print(priv.get_public_key().get_taproot_address().to_string())
    # print(priv.get_public_key().to_taproot_hex())
    # print(len(priv.get_public_key().to_taproot_hex()))

    # print("\n")
    # print(priv.get_public_key().get_address().to_script_pub_key())
    # print(priv.get_public_key().get_address().to_script_pub_key().to_hex())
    # print(priv.get_public_key().get_segwit_address().to_script_pub_key())
    # print(priv.get_public_key().get_segwit_address().to_script_pub_key().to_hex())
    # print(priv.get_public_key().get_segwit_address().to_script_pub_key().to_p2wsh_script_pub_key())
    # print(priv.get_public_key().get_segwit_address().to_script_pub_key().to_p2wsh_script_pub_key().to_hex())
    # print(from_addr.to_script_pub_key().to_hex())
    # print(sk.to_wif())
    # print(sk.get_public_key().get_address().to_string())
    # print(sk.to_bytes())
    # print(sk.to_wif())
    # print(sk.get_public_key().to_hash160())
    # print(sk.get_public_key().)
    # print(sk.get_public_key().to_hex())
    # print(sk.get_public_key().to_hash160())
    # sk2 = PrivateKey('cVFkzuEHQKMv6JhkG4hJeL2RqGMmRjkRjk6HutvMVtE356e8UUdf')
    # print(sk2.get_public_key().to_hex())
    # print(sk2.get_public_key().to_hash160())

    # redeem_script = Script(
    #         ['OP_DUP', 'OP_HASH160', sk.get_public_key().to_hash160(), 'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    # create transaction output using P2PKH scriptPubKey (locking script)
    to_addr = P2trAddress('tb1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqufszhn')
    # script = Script(['OP_DUP', 'OP_HASH160', addr.to_hash160(),
    #                               'OP_EQUALVERIFY', 'OP_CHECKSIG'])

    txout = TxOutput(
        to_satoshis(0.00001),
        to_addr.to_script_pub_key()
    )

    script_code = Script(
        ["OP_DUP", "OP_HASH160", priv.get_public_key().to_hash160(), "OP_EQUALVERIFY", "OP_CHECKSIG"]
    )
    # txout = TxOutput(to_satoshis(0.0003), addr.to_script_pub_key())
    # print(addr.to_script_pub_key().to_hex())
    # create another output to get the change - remaining 0.01 is tx fees
    # note that this time we used to_script_pub_key() to create the P2PKH
    # script
    change_addr = from_addr
    from_amount = to_satoshis(0.00012382)
    change_txout = TxOutput(to_satoshis(0.00011228), change_addr.to_script_pub_key())
    # print(change_addr.to_script_pub_key())
    # special_addr = P2wpkhAddress("2NCxBSjMaVeBFyxmGcD2X428v6k5n3pCQKN")
    # print(special_addr.to_script_pub_key().to_hex())
    # print(change_addr.to_script_pub_key().to_hex())
    #change_txout = TxOutput(to_satoshis(0.29), Script(['OP_DUP', 'OP_HASH160',
    #                                     change_addr.to_hash160(),
    #                                     'OP_EQUALVERIFY', 'OP_CHECKSIG']))

    # create transaction from inputs/outputs -- default locktime is used
    tx = Transaction([txin], [change_txout, txout], has_segwit=False)
    sig = priv.sign_segwit_input(tx, 0, script_code, from_amount)
    tx.witnesses.append(TxWitnessInput([sig, priv.get_public_key().to_hex()]))

    # print raw transaction
    # print("\nRaw unsigned transaction:\n" + tx.serialize())
    # use the private key corresponding to the address that contains the
    # UTXO we are trying to spend to sign the input


    # # note that we pass the scriptPubkey as one of the inputs of sign_input
    # # because it is used to replace the scriptSig of the UTXO we are trying to
    # # spend when creating the transaction digest
    # from_addr = P2wpkhAddress('tb1q9fhs55e9n8v29ml5ztgqlqhujsywdnh4z05v3g')

    # sig = sk.sign_segwit_input( tx, 0, redeem_script, to_satoshis(0.0010))
    #print(sig)

    # # get public key as hex
    # pk = sk.get_public_key().to_hex()

    # # set the scriptSig (unlocking script)
    # # txin.script_sig = Script([sig, pk])
    # tx.witnesses.append( TxWitnessInput([ sig, pk]) )

    signed_tx = tx.serialize()
    print(signed_tx)
    # print raw signed transaction ready to be broadcasted
    # print("\nRaw signed transaction:\n" + signed_tx)

    # # print the size of the final transaction
    # print("\nSigned transaction size (in bytes):\n" + str(tx.get_size()))


if __name__ == "__main__":
    main()



