from bitcointx.core.psbt import PartiallySignedTransaction
from binascii import hexlify, unhexlify

from bitcointx import ChainParams
from bitcointx.core.key import KeyStore, BIP32PathTemplate
from bitcointx.wallet import CCoinKey, CCoinExtKey

from bitcoinutils.setup import setup
from bitcoinutils.keys import P2pkhAddress, P2trAddress, PrivateKey

from bitcointx import select_chain_params

select_chain_params("bitcoin/testnet")
setup('testnet')
psbt = PartiallySignedTransaction.from_base64("cHNidP8BAHcCAAAAAcF9M1TUtf0ej0EVhqlmCnAVen+snm1qFVSn9rBHM2ChAQAAAAD/////AsAnCQAAAAAAGXapFCpvClMlmdii7/QS0A+C/JQI5s71iKwwdQAAAAAAABl2qRSG1d61PCfnfpD9Urfpr8vBcqY7KIisAAAAAAABAN4CAAAAAUQEa8hrE+s55jtVMHPAb4MBs8Owya9bUXbxVVyeT1XyAQAAAGpHMEQCIE906LuoW7Q8FCyxLwi8UbS9+ECe3ggpzwuQw1yO+YS1AiAKdZt6XZWRaf7rLIvZHmeuLtKYsQflJW3C33/I6OjrUgEhA2fIyxqTcyqDl/2Rnomr7eu56Llrid/gbZd2YaldROyt/////wKghgEAAAAAABYAFCpvClMlmdii7/QS0A+C/JQI5s71AMQJAAAAAAAZdqkUKm8KUyWZ2KLv9BLQD4L8lAjmzvWIrAAAAAAAAAA=")
priv = PrivateKey("cUrtpHMVj73rbzBHWfJvv29cP9XUBmBzPXcUg8H8ZJiZhDEZNaxx")
keys = [CCoinKey.from_secret_bytes(priv.to_bytes())]
# print(psbt)
# print(psbt.inputs)
# print(psbt.outputs)
sign_result = psbt.sign(KeyStore.from_iterable(keys), finalize=True)

# print(f'Added signatures to {sign_result.num_inputs_signed} inputs')
# print(f'{sign_result.num_inputs_final} inputs is finalized')
# print(sign_result.num_inputs_ready)
# # print(psbt.get_fee())
# tx = psbt.extract_transaction()
# print(hexlify(tx.serialize()).decode('ascii'))


# from bitcoinutils.transactions import Transaction, TxInput, TxOutput, TxWitnessInput
# tx = Transaction.from_raw("70736274ff0100770200000001c17d3354d4b5fd1e8f411586a9660a70157a7fac9e6d6a1554a7f6b0473360a10100000000fdffffff02c0270900000000001976a9142a6f0a532599d8a2eff412d00f82fc9408e6cef588ac30750000000000001976a91486d5deb53c27e77e90fd52b7e9afcbc172a63b2888ac0000000000000000")
# print(tx)


# bitcoin-cli -testnet walletcreatefundedpsbt "[{\"txid\":\"\",\"vout\":0}]" "[{\"data\":\"00010203\"}]"
