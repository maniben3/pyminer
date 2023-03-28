import numpy as np
import gmpy2
from hashlib import sha256 as hs
from utils import *
from miner import *
from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import array
rpc_user = "pradeep"
rpc_password = "p"
rpc_port = 9912
#
offsets=[1418575498597, 27899359258027, 34460918582347, 76075560855397, 186460616596357, 218021188549267, 234280497145567, 282854319391747, 345120905374117, 346117552180657, 604439135284087, 727417501795087, 1041814617748777, 1090754719898947, 1539765965257777, 3152045700948247, 3323127757029337, 3449427485143897, 4422879865247947, 4525595253334027, 4730773080017857, 5462875671033037, 6147764065076737, 6205707895751467, 6308411019731077, 7582919852522887, 7791180222409687, 9162887985581587, 9305359177794937, 10096106139749887, 10349085616714717, 10744789916260657, 10932016019429377, 11140102475962717, 12448240792011127, 14727257011031437, 16892267700442237, 17963729763800077, 18908121647739427, 19028992697498887, 19756696515786487, 20252223877980967, 20429666791949287, 21680774776901497, 21682173462980287, 23076668788453537, 24036602580170437, 24101684579532817, 25053289894907377, 25309078073142967, 25662701041982107, 25777719656829397, 26056424604564457, 26315911419972277, 26866456999592467, 26887571851660777, 27303559129791817, 27839080743588217, 28595465291933797, 29137316070747757, 30824439453812107, 31395828815154907, 31979851757518537, 32897714831936827 ]

#primes
limit=10**8
primorial =gmpy2.primorial(223)
prime=simpleSieve(limit)
prime= prime[47:]
inv  = np.zeros(len(prime),dtype=np.uint32)
for i in range(len(prime)):
   inv[i]=(int(inverse(primorial,prime[i])))
# 
offset=offsets[0]
 
rpc_connection = AuthServiceProxy(f"http://{rpc_user}:{rpc_password}@138.68.160.201:{rpc_port}/")
block_template = rpc_connection.getblocktemplate({"rules": ["segwit"]})
version = block_template['version']
previous_block_hash = block_template['previousblockhash']
current_time = block_template['curtime']
bits = int(block_template['bits'], 16)
coinbasevalue=block_template['coinbasevalue']
wTxIds = [bytearray(32)]
txHashes=[]
transactionsHex=""
for transaction in block_template["transactions"]:
    txId = hexStrToV8(transaction["txid"])[::-1]
    transactionsHex += transaction["data"]
    txHashes.append(v8ToA8(txId))
    wTxIds.append(v8ToA8(hexStrToV8(transaction["hash"])[::-1]))
de = "6a24aa21a9ed" + v8ToHexStr(a8ToV8(calculateMerkleRoot([calculateMerkleRoot(wTxIds), bytearray(32)])))
if de != block_template["default_witness_commitment"]:
    print("Error"  , block_template['height'])
txcount = len(txHashes)+1
height = block_template['height']
powversion = block_template['powversion']
primeCountTarget = 5
scriptPubKey="0014e2d34d79120698ccb3f76dbbd40b077da52708e0"
coinbase=coinbaseGen(hexStrToV8(scriptPubKey),height, coinbasevalue, hexStrToV8(de))
transactionsHex=v8ToHexStr(coinbase)+transactionsHex
txHashesWithCoinbase = [coinbaseTxId(coinbase)]
txHashesWithCoinbase.extend(txHashes)
dd=calculateMerkleRoot(txHashesWithCoinbase)
merkle = ''.join(hex(byte)[2:].zfill(2) for byte in dd)
print(height)
ddc=str(hex(current_time)[2:])
bh = lit("20000000") + lit(previous_block_hash) + merkle + lit(ddc) +"00000000"+lit(block_template['bits'])
df=bits&255
L = ((10*df*df*df + 7383*df*df + 5840720*df + 3997440) >> 23)
header = bytes.fromhex(bh)
uu=hs(hs(header).digest()).digest().hex()
binary_num = format(L, "08b") # Convert hex_num to 8-bit binary string
binary_num_64 = format(int(lit(uu), 16), "0256b") # Convert hex_num_64 to 64-byte (256-bit) binary string
zero_bits = "0" * (int(decodeBits(bits,1))-264) # Create a string of 768 zero bits
concatenated_binary = "1" + binary_num + binary_num_64 + zero_bits # Concatenate all the binary strings together
T = int(concatenated_binary, 2) # Convert binary string to integer # Convert integer to hex string, and remove the '0x' prefix
print("Target :" ,hex(T))
fac=mine(T,prime,inv,2*10**8,offset)
pnum=48
hex_str = '{:04x}'.format(pnum) + '{:032x}'.format(fac) + '{:024x}'.format(offset) + "0002"