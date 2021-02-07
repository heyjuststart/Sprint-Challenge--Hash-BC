#  Hint:  You may not need all of these.  Remove the unused functions.
from hashtables import (
    HashTable,
    hash_table_insert,
    hash_table_remove,
    hash_table_retrieve,
    hash_table_resize,
)


class Ticket:
    def __init__(self, source, destination):
        self.source = source
        self.destination = destination


def reconstruct_trip(tickets, length):
    hashtable = HashTable(length)
    route = [None] * length

    """
    YOUR CODE HERE
    """

    current_ticket = None
    for ticket in tickets:
        hash_table_insert(hashtable, ticket.source, ticket.destination)
        if ticket.source == "NONE":
            route[0] = ticket.destination

    ticket_index = 0
    while True:
        current_destination = route[ticket_index]
        next_destination = hash_table_retrieve(hashtable, current_destination)
        ticket_index += 1
        route[ticket_index] = next_destination
        if next_destination is "NONE":
            break

    return route
