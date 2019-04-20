class Node(object):
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next = next_node


def has_cycle(head: Node) -> bool:
    previous = head
    current = head.next
    while current:
        if current.next is previous:
            return True
        else:
            previous = current
            current = current.next
    else:
        return False
