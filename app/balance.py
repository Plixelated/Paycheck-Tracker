class balance:
    def __init__(self, __balance):
        self.currentBalance = __balance

    def SetTotal(self, __currentBalance):
        self.currentBalance = __currentBalance
    
    def GetTotal(self):
        return self.currentBalance

    def CalculatePayment(self, __bill):
        return int(self.currentBalance) - int(__bill.total)
