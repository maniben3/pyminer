def hexStrToV8(s):
    if len(s) % 2 != 0:
        s = "0" + s
    v = []
    for i in range(0, len(s), 2):
        byte = int(s[i:i+2], 16)
        v.append(byte)
    return v

def v8ToA8(v8):
    a8 = bytearray(32)
    a8[:len(v8)] = v8[:min(len(v8), 32)]
    return a8

def decodeBits(nBits: int, powVersion: int) -> float:
    if powVersion == 1:
        return float(nBits) / 256.0
    else:
        print("Unexpected PoW Version", powVersion)
        return 1.0

    

cbMsg = "/rM0.93/"

def coinbaseGen(scriptPubKey, height, coinbasevalue, dwc=[]):
    coinbase = bytearray()
    # Version (01000000)
    coinbase.extend([0x01, 0x00, 0x00, 0x00])
    # Marker (00) and Flag (01) for SegWit
    if len(dwc) > 0:
        coinbase.extend([0x00, 0x01])
    # Input Count (01)
    coinbase.append(1)
    # Input TXID (0000000000000000000000000000000000000000000000000000000000000000)
    coinbase.extend([0x00] * 32)
    # Input VOUT (FFFFFFFF)
    coinbase.extend([0xFF] * 4)
    # (ScriptSig Construction)
    scriptSig = bytearray()
    # Block Height (Bip 34)
    if height < 17:
        scriptSig.append(80 + height)
    elif height < 128:
        scriptSig.extend([0x01, height])
    elif height < 32768:
        scriptSig.extend([0x02, height % 256, (height // 256) % 256])
    else:
        scriptSig.extend([0x03, height % 256, (height // 256) % 256, (height // 65536) % 256])
    # Coinbase Message
    for c in cbMsg:
        scriptSig.append(ord(c))
    # Randomization to avoid having 2 threads working on the same problem
    for i in range(4):
        scriptSig.append(0xAB)
    # ScriptSig Size
    coinbase.append(len(scriptSig))
    # ScriptSig
    coinbase.extend(scriptSig)
    # Input Sequence (FFFFFFFF)
    coinbase.extend([0xFF] * 4)
    # Output Count
    coinbase.append(1)
    if len(dwc) > 0:
        coinbase[-1] += 1 # Dummy Output for SegWit
    # Output Value
    reward = coinbasevalue
    for i in range(8):
        coinbase.append(reward % 256)
        reward //= 256
    # Output/ScriptPubKey Length
    coinbase.append(len(scriptPubKey))
    # ScriptPubKey (for the payout address)
    coinbase.extend(scriptPubKey)
    # Dummy output and witness for SegWit
    if len(dwc) > 0:
        coinbase.extend([0] * 8) # No reward
        coinbase.append(len(dwc)) # Output Length
        coinbase.extend(dwc) # Default Witness Commitment
        coinbase.append(1) # Number of Witnesses/stack items
        coinbase.append(32) # Witness Length
        coinbase.extend([0x00] * 32) # Witness of the Coinbase Input (0000000000000000000000000000000000000000000000000000000000000000)
    # Lock Time (00000000)
    coinbase.extend([0x00] * 4)
    return coinbase
def reverse(c):
    return c[::-1]
def a8ToV8(a8):
    return list(a8)

import hashlib
from typing import List

def sha256(data: bytes) -> bytes:
    sha = hashlib.sha256()
    sha.update(data)
    return sha.digest()

def sha256sha256(data: bytes) -> bytes:
    return sha256(sha256(data))
def v8ToHexStr(v):
    return ''.join(format(x, '02x') for x in v)

from typing import List
import binascii

def reverse(s: bytes) -> bytes:
    return s[::-1]

def hexStrToV8(hexStr: str) -> bytes:
    return binascii.unhexlify(hexStr)

def v8ToA8(v8: bytes) -> bytearray:
    return bytearray(v8)


def primegen(n):
    primes = []
    for i in range(2, n):
        if gmpy2.is_prime(i):
            primes.append(i)
    return primes
  
def lit(hex_str) :   
    
  byte_str = bytes.fromhex(hex_str)
  le_byte_str = byte_str[::-1]
  le_hex_str = le_byte_str.hex()
  return le_hex_str
  
def decodeBits(nBits: int, powVersion: int) -> float:
    if powVersion == 1:
        return float(nBits) / 256.0
    else:
        print("Unexpected PoW Version", powVersion)
        return 1.0
import hashlib
from typing import List

def coinbaseTxId(coinbase):
    coinbase2 = bytearray()
    for i in range(4):
        coinbase2.append(coinbase[i])
    for i in range(6, len(coinbase) - 38):
        coinbase2.append(coinbase[i])
    for i in range(len(coinbase) - 4, len(coinbase)):
        coinbase2.append(coinbase[i])
    return hashlib.sha256(hashlib.sha256(bytes(coinbase2)).digest()).digest()

def calculateMerkleRoot(txHashes: List[bytes]) -> bytes:
    merkleRoot = b''
    if len(txHashes) == 0:
        print("No transaction to hash")
    elif len(txHashes) == 1:
        return txHashes[0]
    else:
        txHashes2 = []
        for i in range(0, len(txHashes), 2):
            concat = txHashes[i]
            if i == len(txHashes)-1: # Concatenation of the last element with itself for an odd number of transactions
                concat = concat+txHashes[i]
            else:
                concat += txHashes[i +1]
            txHashes2.append(hashlib.sha256(hashlib.sha256(concat).digest()).digest())
        # Process the next step
        merkleRoot = calculateMerkleRoot(txHashes2)
    return merkleRoot
