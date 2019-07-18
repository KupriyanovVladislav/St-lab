class Node:
    def __init__(self, data):
        self.data = data
        self.left = None
        self.right = None


def checkBST(root: Node, left=None, right=None) -> bool:
    if not root:
        return True

    if left:
        if root.data <= left.data:
            return False

    if right:
        if root.data >= right.data:
            return False

    return checkBST(root.left, left, root) and checkBST(root.right, root, right)


# def checkBST(root: Node, prev=None):
#     if not root:
#         return True
#
#     elif root.left:
#         if not(root.data > root.left.data):
#             return False
#         elif prev and root.left.data < prev.data and root.right.data < prev.data:
#             return False
#
#     elif root.right:
#         if not (root.data < root.right.data):
#             return False
#         elif prev and prev.data < root.right.data and prev.data < root.left.data:
#             return False
#
#
#     return checkBST(root.left, root) and checkBST(root.right, root)


if __name__ == '__main__':
    root = Node(4)
    root.left = Node(2)
    root.left.left = Node(1)
    root.left.right = Node(3)
    root.right = Node(6)
    root.right.left = Node(5)
    root.right.right = Node(7)
    if (checkBST(root)):
        print("Is BST")
    else:
        print("Not a BST") 
