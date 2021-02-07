import requests

import sys

from uuid import uuid4

from timeit import default_timer as timer

import hashlib
import random

hash_dict = {}


def proof_of_work(last_proof):
    """
    Multi-Ouroboros of Work Algorithm
    - Find a number p' such that the last six digits of hash(p) are equal
    to the first six digits of hash(p')
    - IE:  last_hash: ...999123456, new hash 123456888...
    - p is the previous proof, and p' is the new proof
    """

    start = timer()

    print("Searching for next proof")
    proof = random.randint(0, sys.maxsize / 1000)
    #  TODO: Your code here
    last_hash = do_hash(last_proof)
    while valid_proof(last_hash, proof) is False:
        if timer() - start > 10:
            return None
        proof += 1


    print("Proof found: " + str(proof) + " in " + str(timer() - start))
    return proof

def do_hash(number):
    if number in hash_dict:
        return hash_dict[number]
    else:
        new_one = hashlib.sha256(f'{number}'.encode()).hexdigest()
        hash_dict[number] = new_one
        return new_one



def valid_proof(last_hash, proof):
    """
    Validates the Proof:  Multi-ouroborus:  Do the last six characters of
    the last hash match the first six characters of the proof?

    IE:  last_hash: ...999123456, new hash 123456888...
    """

    # TODO: Your code here!
    # hash_int
    # last_hash = hashlib.sha256(f'{last_hash}'.encode()).hexdigest()
    # this_hash = hashlib.sha256(f'{proof}'.encode()).hexdigest()
    this_hash = do_hash(proof)

    return this_hash[:6] == last_hash[-6:]



old_proof = None
if __name__ == '__main__':
    # What node are we interacting with?
    if len(sys.argv) > 1:
        node = sys.argv[1]
    else:
        node = "https://lambda-coin.herokuapp.com"

    coins_mined = 0

    # Load or create ID
    f = open("my_id.txt", "r")
    id = f.read()
    # id = "0408a67231eb45c1b965bf9dfb7ee334"
    print("ID is", id)
    f.close()
    if len(id) == 0:
        f = open("my_id.txt", "w")
        # Generate a globally unique ID
        id = str(uuid4()).replace('-', '')
        print("Created new ID: " + id)
        f.write(id)
        f.close()
    # Run forever until interrupted
    while True:
        # Get the last proof from the server
        r = requests.get(url=node + "/last_proof")
        data = r.json()
        # last_proof = data.get('proof')
        # print(last_proof)
        # new_proof = last_proof
        # if int(last_proof) == 4029359:
        #     new_proof = 99747858623040
        # else:
        #     new_proof = 4029359
        new_proof = proof_of_work(data.get('proof'))

        # continue if new_proof is None (ran outta time)
        if new_proof is None:
            continue

        post_data = {"proof": new_proof,
                     "id": id}

        r = requests.post(url=node + "/mine", json=post_data)
        data = r.json()
        if data.get('message') == 'New Block Forged':
            coins_mined += 1
            print("Total coins mined: " + str(coins_mined))
        else:
            print(data.get('message'))
