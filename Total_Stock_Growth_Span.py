class StockSpanner(object):

    def __init__(self):
        self.stack = []
        self.paststreak = []
        self.streak = 0
        
        

    def next(self, price):
        """
        :type price: int
        :rtype: int
        """
        while self.stack:
            if self.stack[-1] > price:
                self.paststreak.append([self.stack.pop(), self.streak])
                self.streak = 0
            else:
                break
        self.stack.append(price)
        self.streak += 1
        streak = self.streak
        for i in range(1, len(self.paststreak) + 1):
            if price >= self.paststreak[-i][0]:
                streak += self.paststreak[-i][1]
            else:
                break
        return streak
        


# Your StockSpanner object will be instantiated and called as such:
# obj = StockSpanner()
# param_1 = obj.next(price)