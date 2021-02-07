import sys
from timeit import default_timer as timer
import hashlib
import random


def proof_of_work(last_proof, starting_pt):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = timer()

    # print("Searching for next proof")
    last_hash = hashlib.sha256(f'{last_proof}'.encode()).hexdigest()
    proof = starting_pt
    #  TODO: Your code here
    while valid_proof(last_hash, proof) is False:
        proof += 1


    # print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof


def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    # TODO: Your code here!
    this_hash = hashlib.sha256(f'{proof}'.encode()).hexdigest()
    return this_hash[:6] == last_hash[-6:]


# read sys_arg
last_proof = sys.argv[1]
offset = sys.argv[2]
num_threads = sys.argv[3]
block_size = sys.maxsize // int(num_threads)
starting_point = 0 + (block_size * int(offset))

print(proof_of_work(last_proof, starting_point))
# print("Hi")
