class Node:

    def __init__(self, data, prev=None, next=None):
        """
        Sets the initial state of self.
        :param data: the value of the node
        :param prev: the previous node
        :param next: the next node
        """
        self.data = data
        self.prev = prev
        self.next = next

    def get_data(self):
        return self.data

    def get_prev(self):
        return self.prev

    def get_next(self):
        return self.next

    def set_data(self, value):
        self.data = value

    def set_prev(self, value):
        self.prev = value

    def set_next(self, value):
        self.next = value

    def __str__(self):
        return str(self.data)