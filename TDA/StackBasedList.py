class StackListBased:
    """ Implementation of ADT Stack based on Python type list. """

    def __init__(self):
        """
        Sets the initial state of self.
        """
        self._items = []

    # collection accessor methods

    def is_empty(self):
        """
        Tests if self is empty.
        :return: True if len(self) is 0, otherwise False
        """
        return len(self._items) == 0

    def __len__(self):
        """
        Gets the number of items in self.
        :return: the number of items in self
        """
        return len(self._items)

    def __str__(self):
        """
        Builds the string representation of self.
        :return: String representation of self
        """
        return str(self._items)

    def __iter__(self):
        """
        Supports iteration over a view of self.
        :return: an iteration of self
        """
        return iter(self._items)

    # collection mutator methods

    def clear(self):
        """
        Makes self become empty.
        :return: None
        """
        self._items = []

    # Stack accessor methods

    def peek(self):
        """
        Gets the item at the top of the stack, assuming the stack is not empty.
        :return: the top item
        """
        return self._items[len(self._items) - 1]

    # Stack mutator methods

    def push(self, item):
        """
        Inserts item at the top of the stack.
        :param item: the item to insert
        :return: None
        """
        self._items.append(item)

    def pop(self):
        """
        Removes the item at top of the stack, assuming the stack is not empty
        :return the item removed
        """
        return self._items.pop()
