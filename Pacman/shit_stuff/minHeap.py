class MinHeap:
    def __init__(self) -> None:
        self.items = []
    
    def push(self, item, criteria):
        i = 0
        if self.items == []:
            self.items.append((item, criteria))
        else:
            while i < len(self.items) and criteria > self.items[i][1]:
                i += 1
            self.items.insert(i, (item, criteria))
    
    def pop(self):
        return self.items[0]

    def size(self):
        return len(self.items)
    
    def is_element(self, item):
        for i in self.items:
            if item == i[0]:
                return True
        return False

    def remove(self, item):
        self.items.remove(item)
    
m = MinHeap()

m.push(0, 1)
m.push(0, 5)
m.push(0, 3)
print(m.items)
print(m.pop())