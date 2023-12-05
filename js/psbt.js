const bitcoin = require('bitcoinjs-lib')
const psbt = new bitcoin.Psbt({ network: bitcoin.networks.testnet }) 
// console.log(psbt.toHex())
const {BIP32Factory} = require('bip32');
const bip39 = require('bip39');
// import { Signer, SignerAsync, ECPairInterface, ECPairFactory, ECPairAPI, TinySecp256k1Interface } from 'ecpair';
const tinysecp = require('tiny-secp256k1');
bitcoin.initEccLib(tinysecp)
const {ECPairFactory} = require('ecpair');
const ECPair = ECPairFactory(tinysecp)
const bip32 = BIP32Factory(tinysecp);
// For Mainnet: const psbt = new bitcoin.Psbt({ network: bitcoin.networks.bitcoin })
// const { ECPair } = require('ecpair');
// example transaction
const unspentOutput = {
  "txid": "512d543a44f4785fe4dcf39d01d753602817142a96c993a22ec434e840129d6d",
  "vout": 1,
  "address": "2NCxBSjMaVeBFyxmGcD2X428v6k5n3pCQKN",
  "label": "payment",
  "redeemScript": "00142a6f0a532599d8a2eff412d00f82fc9408e6cef5",
  "scriptPubKey": "0020159c093089510f88d1d31e1b0aef63afd2037062671096a42348be6e465ee739",
  "amount": 9000,
  "confirmations": 24,
  "spendable": true,
  "solvable": true,
  "desc": "sh(wpkh([7fc5659a/0'/0'/1']02284916d8cd4fdf35574d5f0aaea0c93607254b06601ef126e73d8fb075b7169f))#6k9sssw6",
  "safe": true
}
// get transaction hex
// You can use any public API to get it...
// https://testnet-api.smartbit.com.au/v1/blockchain/transaction/11e5b7005a76c8a53f9a0036bc1a2745ebd73ad40017b3169894aa2c19e789d7/hex
var rawTransaction = "020000000001019ec94aac879a6bb22d377e293a9ba1c277734b3b480c1efb863019e9803bb4d30000000000ffffffff02e803000000000000225120cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382e5e300000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a130247304402204be363a611690c2a4259c52b1fc681b80846f78b675a40025dd2661473bba651022072f5fd61dd8460e3970b80fd9ed10a15aad98b68800a47a7591be5a18767a8c7012102303cb0fa91142140ba67f05979304334d69ce6aed51c32e58294cc05629e003000000000"
const isSegwit = rawTransaction.substring(8, 12) === '0001'
// console.log(isSegwit)
const network = bitcoin.networks.testnet

// function tweakSigner(signer: Signer, opts: any = {}): Signer {
//     // eslint-disable-next-line @typescript-eslint/ban-ts-comment
//     // @ts-ignore
//     let privateKey: Uint8Array | undefined = signer.privateKey!;
//     if (!privateKey) {
//         throw new Error('Private key is required for tweaking signer!');
//     }
//     if (signer.publicKey[0] === 3) {
//         privateKey = tinysecp.privateNegate(privateKey);
//     }

//     const tweakedPrivateKey = tinysecp.privateAdd(
//         privateKey,
//         tapTweakHash(toXOnly(signer.publicKey), opts.tweakHash),
//     );
//     if (!tweakedPrivateKey) {
//         throw new Error('Invalid tweaked private key!');
//     }

//     return ECPair.fromPrivateKey(Buffer.from(tweakedPrivateKey), {
//         network: opts.network,
//     });
// }
// if (!isSegwit) {
//     psbt.addInput({
//         hash: unspentOutput.txid,
//         index: unspentOutput.vout,
//         witnessUtxo: {
//             script: Buffer.from("76a9142a6f0a532599d8a2eff412d00f82fc9408e6cef588ac", 'hex'),
//             value: unspentOutput.amount // value in satoshi
//         },
//         redeemScript: Buffer.from(unspentOutput.redeemScript, 'hex'),
//         // witnessScript: Buffer.from("159c093089510f88d1d31e1b0aef63afd2037062671096a42348be6e465ee739", 'hex')
//     })
// } else {
//     console.log("here")
//     psbt.addInput({
//         hash: unspentOutput.txid,
//         index: unspentOutput.vout,
//         nonWitnessUtxo: Buffer.from(rawTransaction, 'hex')
//         // redeemScript: Buffer.from("2a6f0a532599d8a2eff412d00f82fc9408e6cef5", 'hex')
//     })
// }

// add output - destination address and the amount to transfer to
// psbt.addOutput({
//   address: "tb1q026q3uact4p062cq95057mme43h462sn2cpkes",
//   value: 1000 // value in satoshi (0.5 BTC)
// })
// If we look closely, We have input of 1 BTC and we are trying to send 0.5 BTC
// If we just use these configurations to send the transaction, it will consume remaining 0.5 BTC as fees
// which we wouldn't want
// So we'll leave some fee for the transaction, let's say 0.001 BTC and send the remaining amount to change address
// change address is the address you own where change from the transaction can be sent to
// psbt.addOutput({
//   address: "tb1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqufszhn", 
//   value: 12000 // value in satoshi (0.499 BTC)
// })

// console.log(psbt.toBase64())
// console.log(psbt.txInputs)
// console.log(psbt.txOutputs)
// create transaction end

function tapTweakHash(pubKey, h) {
  return bitcoin.crypto.taggedHash(
      'TapTweak',
      Buffer.concat(h ? [pubKey, h] : [pubKey]),
  );
}

function toXOnly(pubkey) {
  return pubkey.subarray(1, 33)
}

// function tweakSigner(signer, opts) {
//   // eslint-disable-next-line @typescript-eslint/ban-ts-comment
//   // @ts-ignore
//   var privateKey = signer.privateKey;
//   if (!privateKey) {
//       throw new Error('Private key is required for tweaking signer!');
//   }
//   if (signer.publicKey[0] === 3) {
//       privateKey = tinysecp.privateNegate(privateKey);
//   }

//   const tweakedPrivateKey = tinysecp.privateAdd(
//       privateKey,
//       tapTweakHash(signer.publicKey.slice(1, 33), false),
//   );
//   if (!tweakedPrivateKey) {
//       throw new Error('Invalid tweaked private key!');
//   }

//   return ECPair.fromPrivateKey(Buffer.from(tweakedPrivateKey), {
//       network: opts.network,
//   });
// }

async function fun() {
    // const xprv =
    //     'xprv9s21ZrQH143K3GJpoapnV8SFfukcVBSfeCficPSGfubmSFDxo1kuHnLisriDvSnRRuL2Qrg5ggqHKNVpxR86QEC8w35uxmGoggxtQTPvfUu';
    // Path to first child of receiving wallet on first account
    // const internalPubkey = Buffer.from(
    //     'cc8a4bc64d897bddc5fbc2f670f7a8ba0b386779106cf1223c6fc5d7cd6fc115',
    //     'hex',
    // );
    // const expectedAddress =
    //     'bc1p5cyxnuxmeuwuvkwfem96lqzszd02n6xdcjrs20cac6yqjjwudpxqkedrcr';

    // Verify the above (Below is no different than other HD wallets)
    const path = `m/86'/0'/0'/0/0`; 
    const mnemonic = 'border payment tide also window catalog winner artwork fit bamboo culture hurt';
    const seed = await bip39.mnemonicToSeed(mnemonic)
    const rootKey = bip32.fromSeed(seed)
    const childNode = rootKey.derivePath(path);
    // assert.strictEqual(rootKey.toBase58(), xprv);
    // Since internalKey is an xOnly pubkey, we drop the DER header byte
    const childNodeXOnlyPubkey = toXOnly(childNode.publicKey);
    const network = bitcoin.networks.testnet
    // console.log(keypair.publicKey.slice(1, 33))
    // const childNodeXOnlyPubkey = keypair.publicKey.slice(1, 33)
    // console.log(childNodeXOnlyPubkey)
    // const keypair = ECPair.fromWIF("cSXYFN4N7ZnGW5Kt9YcSKbpaaoSxAFCUnmZCKNgV7H5XWPkEyou5", network)
    // // const keypair = ECPair.fromWIF("c........", network)
    // const tweakedSigner = tweakSigner(keypair, { network: network });

    // const {address, output} = bitcoin.payments.p2tr({
    //     // pubkey: Buffer("cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382e", "hex"),
    //     pubkey: toXOnly(tweakedSigner.publicKey),
    //     network: network
    // });


    
    // console.log(p2pktr.address)
    // console.log(p2pktr.output)
    // console.log("hi")
    // const p2pktr = bitcoin.payments.p2tr({
    //     childNodeXOnlyPubkey, network
    // });
    // console.log(address)
    const tweakedChildNode = childNode.tweak(
        bitcoin.crypto.taggedHash('TapTweak', childNodeXOnlyPubkey),
    );


 
    // const psbt = bitcoin.Psbt.fromHex("70736274ff01007d02000000019ec94aac879a6bb22d377e293a9ba1c277734b3b480c1efb863019e9803bb4d30000000000ffffffff02e803000000000000225120cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382e5e300000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a13000000000001011fe0340000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a1301086b0247304402204be363a611690c2a4259c52b1fc681b80846f78b675a40025dd2661473bba651022072f5fd61dd8460e3970b80fd9ed10a15aad98b68800a47a7591be5a18767a8c7012102303cb0fa91142140ba67f05979304334d69ce6aed51c32e58294cc05629e0030000000")
    
    const amount = 2556
    function tweakSigner(signer) {
      return signer.tweak(
        bitcoin.crypto.taggedHash("TapTweak", toXOnly(signer.publicKey))
      );
    }

    const keypair = ECPair.fromWIF("cSXYFN4N7ZnGW5Kt9YcSKbpaaoSxAFCUnmZCKNgV7H5XWPkEyou5", network)
    const tweakedSigner = tweakSigner(keypair, { network: network });

    const p2pktr = bitcoin.payments.p2tr({
      pubkey: toXOnly(tweakedSigner.publicKey),
      network
    });

    psbt.addInput({
      hash: "91bde19ea2caebc8143431f0d2545947349fd42ab5809968bca4b9a744c2bec6",
      index: 1,
      witnessUtxo: { value: amount, script: p2pktr.output },
      tapInternalKey: toXOnly(tweakedSigner.publicKey),
    })
    .addOutput({
      value: 1000,
      address: "tb1q026q3uact4p062cq95057mme43h462sn2cpkes",
    }).addOutput({
      value: 1412,
      address: "tb1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqufszhn"
    })  

    console.log(psbt.toHex())
    console.log(tweakedSigner.publicKey)
    console.log(keypair.publicKey)
    //{publicKey: toXOnly(tweakedSigner.publicKey), network: network}
    psbt.signAllInputs(tweakedSigner).finalizeAllInputs()
    console.log(psbt.toHex())


  const tx = psbt.extractTransaction();
  console.log(tx.toHex())  
  console.log(tx.byteLength())
  // console.log("end")
  // console.log(psbt.txInputs)
  // console.log(psbt.txOutputs)
  // console.log(psbt.toBase64())
  // console.log("real end")

    const newpsbt = bitcoin.Psbt.fromHex("70736274ff01007d0200000001c6bec244a7b9a4bc689980b52ad49f34475954d2f0313414c8ebcaa29ee1bd910100000000ffffffff02e8030000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a138405000000000000225120cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382e000000000001012bfc09000000000000225120cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382e010842014030b5f1ba70dc7e547f1ae4a76c4cb0b5547f684af2fb474d9074c7f442d42a3b512e00e34beec29e3c669a9cdedbe3a662e13e163e54f039c83f4f2ff7fad535000000", {network: network})
    // newpsbt.signAllInputs(tweakedSigner).finalizeAllInputs()
    console.log(newpsbt.extractTransaction().virtualSize())
    console.log(newpsbt.toHex())
    
    // console.log(newpsbt.txInputs)
    // console.log(newpsbt.txOutputs)
    // console.log(newpsbt.toBase64())
}

fun()
return
// This is new for taproot
// Note: we are using mainnet here to get the correct address
// The output is the same no matter what the network is.
// const { address, output } = bitcoin.payments.p2tr({
//     internalPubkey,
// });

// // const tweakedSigner = tweakSigner(keypair, { network });

function toXOnly(pubkey) {
    return pubkey.subarray(1, 33)
}

// const p2pktr = bitcoin.payments.p2tr({
//     pubkey: toXOnly(keypair.publicKey),
//     network
// });

console.log(psbt.toHex())
console.log("here0")

const keypair = ECPair.fromWIF("cRUGeuFL552ty3WcmgyNxvmJgufQuuRqGXNx65h5Bh9tvd2xx74P", network)

psbt.addInput({
        hash: "ee9c24e8cf2fb940aa72bd3307da6d500049e3bfbc640c40f0ff26f2c0cb8da0",
        index: 1,
        nonWitnessUtxo: Buffer.from(rawTransaction, 'hex')
        // witnessUtxo: { value: 13686, script: p2pktr.output },
        // tapInternalKey: toXOnly(keypair.publicKey)
});

psbt.addOutput({
    address: "tb1pe5282cps0z72y5clmkzv0d9yrcdq5nqa29gt83ncewun8zc28qhqufszhn",
    value: 1000
});

psbt.addOutput({
    address: "tb1q026q3uact4p062cq95057mme43h462sn2cpkes",
    value: 12382-1000-154
});

console.log(psbt.toHex())
console.log("here")
psbt.signAllInputs(keypair).finalizeAllInputs()
console.log(psbt.toHex())
console.log("here")
// // psbt.signInput(0, ECPair.fromWIF("cRUGeuFL552ty3WcmgyNxvmJgufQuuRqGXNx65h5Bh9tvd2xx74P", network))
// // you can use validate signature method provided by library to make sure generated signature is valid
// // psbt.validateSignaturesOfAllInputs() // if this returns false, then you can throw the error
// psbt.finalizeAllInputs()
// // signed transaction hex
// console.log(psbt.txInputs)
// console.log(psbt.txOutputs)
const transaction = psbt.extractTransaction()
const signedTransaction = transaction.toHex()
console.log(signedTransaction)
console.log("end")
const psbt2 = bitcoin.Psbt.fromHex("70736274ff01007d0200000001a08dcbc0f226fff0400c64bcbfe34900506dda0733bd72aa40b92fcfe8249cee0100000000ffffffff02e803000000000000225120cd1475603078bca2531fdd84c7b4a41e1a0a4c1d5150b3c678cbb9338b0a382edc2b0000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a13000000000001011f5e300000000000001600147ab408f3b85d42fd2b002d1f4f6f79ac6f5d2a1301086c0248304502210083c8344dc36bdd5ab77cc685bb96d5ecfe8e91f0c25f72bb53ed48bcb63a0d490220426afb32e00bcbc37181c088ba10555fbc33727368b474f9b056388fb6fce1bd012102303cb0fa91142140ba67f05979304334d69ce6aed51c32e58294cc05629e0030000000")
// console.log(psbt2.txInputs)
// console.log(psbt2.txOutputs)
console.log(psbt == psbt2)
console.log(psbt2.extractTransaction().toHex())
// console.log(signedTransaction)
// const transactionId = transaction.getId()
// sign transaction end