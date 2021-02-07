#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (HashTable,
                        hash_table_insert,
                        hash_table_remove,
                        hash_table_retrieve,
                        hash_table_resize)


def get_indices_of_item_weights(weights, length, limit):
    ht = HashTable(16)

    """
    YOUR CODE HERE
    """
    index = 0
    for w in weights:
        # get the weight difference from the limit, check if that
        # exists
        weight_diff = limit - w
        possible_answer = hash_table_retrieve(ht, weight_diff)
        if possible_answer is not None:
            # check which is >
            if index > possible_answer:
                return (index, possible_answer)
            else:
                return (possible_answer, index)
        hash_table_insert(ht, w, index)
        index += 1

    return None


def print_answer(answer):
    if answer is not None:
        print(f"[{answer[0]} {answer[1]}]")
        # print(str(answer[0] + " " + answer[1]))
    else:
        print("None")

# weights = [ 4, 6, 10, 15, 16 ]
# weights = [4,4]
# weights = [12, 6, 7, 14, 19, 3, 0, 25, 40]
# length = 9
# limit = 7
#
# print_answer(get_indices_of_item_weights(weights, length, limit))
