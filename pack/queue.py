import copy
class Queue(object):
    def __init__(self, *args):
        self.queue = []
    def put(self,item):
        """
        入队列
        """
        self.queue.append(item)
    def get(self):
        """
        出队列
        """
        first = copy.deepcopy(self.queue[0])
        self.queue.pop(0)
        return first
    def find(self,number):
        """
        查找
        """
        return self.queue[number]

    def size(self):
        """
        返回队列大小
        """
        return len(self.queue)