class QueueBasedList:

    def __init__(self):
        self.queue = []

    def is_empty(self):
        """
        Tests if self is empty.
        :return: True if len(self) is 0, otherwise False
        """
        return len(self.queue) == 0

    def __len__(self):
        """
        Gets the number of items in self.
        :return: the number of items in self
        """
        return len(self.queue)

    def __str__(self):
        """
        Builds the string representation of self.
        :return: String representation of self
        """
        return str(self.queue)

    def __iter__(self):
        """
        Supports iteration over a view of self.
        :return: an iteration of self
        """
        return iter(self.queue)

    # collection mutator methods

    def clear(self):
        """
        Makes self become empty.
        :return: None
        """
        self.queue = []

    # Queue accessor methods

    def peek(self):
        """
        Gets the item at the top of the queue, assuming the queue is not empty.
        :return: the top item
        """
        return self.queue[0]

    # Queue mutator methods

    def add(self, item):
        """
        Inserts item at the rear of the queue.
        :param item: the item to insert
        :return: None
        """
        self.queue.append(item)

    def pop(self):
        """
        Removes the item at top of the queue, assuming the queue is not empty.
        :return the item removed
        """
        if not self.is_empty():
            return self.queue.pop(0)
