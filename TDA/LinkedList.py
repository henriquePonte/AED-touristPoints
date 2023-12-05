from TDA import node
Node = node.Node


class LinkedList:
    def __init__(self):
        self.head = None

    def __str__(self):
        if self.is_empty():
            return "Linked List is empty"
        else:
            current = self.head
            result = ""
            while current is not None:
                result += str(current.data) + " -> "
                current = current.next
            result += "None"
            return result

    def is_empty(self):
        return self.head is None

    def append(self, data):
        """
        Adiciona um elemento no fim da lista.
        :param data: Adiciona um novo nó com o valor data
        :return:
        """
        new_node = Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node

    def prepend(self, data):
        """
        Adiciona um elemento no início)
        :param data: Adiciona um novo nó com o valor data
        :return:
        """
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def pop(self, data):
        if self.is_empty():
            return "lista vazia"

        if self.head.data == data:
            self.head = self.head.next
            return "Nó removido"

        current = self.head
        while current.next is not None:
            if current.next.data == data:
                current.next = current.next.next
                return
            current = current.next

    def find_by_key(self, key):
        curr_node = self.head
        while curr_node:
            if curr_node.data.nome == key:
                return curr_node.data
            curr_node = curr_node.next
        return None

    def __len__(self):
        count = 0
        current = self.head
        while current is not None:
            count += 1
            current = current.next
        return count

    def get_all(self):
        all_data = []
        current = self.head
        while current:
            all_data.append(current.data)
            current = current.next
        return all_data

    def to_list(self):
        """
        Retorna uma lista com os elementos da lista encadeada.
        """
        result = []
        current = self.head
        while current is not None:
            result.append(current.data)
            current = current.next
        return result