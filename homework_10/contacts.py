class Node:
    def __init__(self, symbol):
        self.symbol = symbol
        self.children = []
        self.counter = 0

    def get_child(self, symbol: str):

        for child in self.children:

            if child.symbol == symbol:
                return child

        return None


class Trie:

    def __init__(self):
        self.root = Node('*')

    def add(self, contact: str):
        current = self.root

        for char in contact:
            next_node = current.get_child(char)

            if not next_node:
                next_node = Node(char)
                current.children.append(next_node)

            next_node.counter += 1
            current = next_node

    def find(self, contact: str):
        current = self.root

        for char in contact:
            next_node = current.get_child(char)
            if not next_node:
                return 0

            current = next_node

        return current.counter


if __name__ == '__main__':
    contacts = Trie()

    n = int(input())

    for n_itr in range(n):
        opContact = input().split()

        op = opContact[0]

        contact = opContact[1]

        if op == 'add':
            contacts.add(contact)

        elif op == 'find':
            print(contacts.find(contact))
