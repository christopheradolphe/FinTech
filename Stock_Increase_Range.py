class StockSpanner(object):

    def __init__(self):
        self.stack = []
        self.streak = 0
        
        

    def next(self, price):
        """
        :type price: int
        :rtype: int
        """
        while self.stack:
            if self.stack[-1] > price:
                self.stack.pop()
                self.streak = 0
            else:
                break
        self.stack.append(price)
        self.streak += 1
        return self.streak