# '''
# Linked List hash table key/value pair
# '''


class LinkedPair:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None

    def __str__(self):
        return f'(key: {self.key}, value: {self.value}) -> {self.next}'


class HashTable:
    '''
    A hash table that with `capacity` buckets
    that accepts string keys
    '''
    def __init__(self, capacity):
        self.original_capacity = capacity
        self.capacity = capacity  # Number of buckets in the hash table
        self.storage = [None] * capacity
        self.resizing = False

    def __str__(self):
        output = ''
        for x in range(0, len(self.storage)):
            output += f'{self.storage[x]} \n'
        return output

    def _hash(self, key):
        '''
        Hash an arbitrary key and return an integer.
        You may replace the Python hash with DJB2 as a stretch goal.
        '''
        return hash(key)

    def _hash_djb2(self, key):
        '''
        Hash an arbitrary key using DJB2 hash
        OPTIONAL STRETCH: Research and implement DJB2
        '''
        pass

    def _hash_mod(self, key):
        '''
        Take an arbitrary key and return a valid integer index
        within the storage capacity of the hash table.
        '''
        return self._hash(key) % self.capacity

    def insert(self, key, value):
        '''
        Store the value with the given key.
        Hash collisions should be handled with Linked List Chaining.
        Fill this in.
        '''

        hash_index = self._hash_mod(key)
        loc = self.storage[hash_index]
        linked_pair = LinkedPair(key, value)
        if not hasattr(loc, 'key'):
            self.storage[hash_index] = linked_pair
            self.resize()
            return True
        while loc is not None:
            if loc.key == key:
                loc.value = value
                self.resize()
                return True
            if loc.next is None:
                loc.next = linked_pair
                self.resize()
                return True
            loc = loc.next

    def remove(self, key):
        '''
        Remove the value stored with the given key.
        Print a warning if the key is not found.
        Fill this in.
        '''
        if not key: return False
        hash_index = self._hash_mod(key)
        loc = self.storage[hash_index]
        prev = None
        while loc is not None:
            if loc.key == key:
                next_link = loc.next
                if prev is not None: prev.next = next_link
                else: self.storage[hash_index] = next_link
                loc.next = None
                self.resize()
                return True
            prev = loc
            loc = loc.next
        return False

    def retrieve(self, key):
        '''
        Retrieve the value stored with the given key.
        Returns None if the key is not found.
        Fill this in.
        '''

        if not key: return None
        hash_mod = self._hash_mod(key)
        loc = self.storage[hash_mod]
        while loc is not None:
            if loc.key == key:
                return loc.value
            loc = loc.next
        return None

    def get_load_factor(self):
        count = 0
        for x in range(0, len(self.storage)):
            current = self.storage[x]
            if not hasattr(current, 'key'): continue
            while current is not None:
                count += 1
                current = current.next
        return count / len(self.storage)

    def copy_storage(self, capacity):
        self.resizing = True
        old_storage = self.storage
        self.storage = [None] * capacity
        self.capacity = capacity
        for index in range(0, len(old_storage)):
            current_link = old_storage[index]
            if not hasattr(current_link, 'key'): continue
            while current_link is not None:
                self.insert(current_link.key, current_link.value)
                current_link = current_link.next
        self.resizing = False

    def resize(self):
        '''
        Doubles the capacity of the hash table and
        rehash all key/value pairs.
        Fill this in.
        '''
        if self.resizing: return
        load_factor = self.get_load_factor()
        if load_factor < 0.2 and self.capacity > self.original_capacity:
            # halve size of storage and reapply all linked pairs
            new_capacity = int(self.capacity / 2)
            self.copy_storage(new_capacity)
        if load_factor > 0.8:
            new_capacity = int(self.capacity * 2)
            self.copy_storage(new_capacity)


if __name__ == "__main__":
    ht = HashTable(2)

    old_capacity = len(ht.storage)

    ht.insert("line_1", "Tiny hash table")
    ht.insert("line_2", "Filled beyond capacity")
    ht.insert("line_3", "Linked list saves the day!")
    ht.insert("line_4", "Linked list saves the day!")
    ht.insert("line_5", "Linked list saves the day!")
    ht.insert("line_6", "Linked list saves the day!")
    ht.insert("line_7", "Linked list saves the day!")
    ht.insert("line_8", "Linked list saves the day!")
    print("")

    # Test storing beyond capacity
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    # Test resizing
    ht.resize()
    new_capacity = len(ht.storage)

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    print(ht.retrieve("line_1"))
    print(ht.retrieve("line_2"))
    print(ht.retrieve("line_3"))

    print("")
