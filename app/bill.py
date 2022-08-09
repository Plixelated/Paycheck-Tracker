class bill:
    def __init__(self, __name, __total, __date):
        self.name = __name
        self.total = __total
        if __date != None:
            self.date = __date
        else:
            self.date = None
        self.pay = False
        self.bill = {}
    
    def SetPaymentStatus(self, __paymentStatus):
        self.pay = __paymentStatus
    
    def GetPaymentStatus(self):
        return self.paid
    
    def GetTotal(self):
        return self.total
    
    def GetName(self):
        return self.name
    
    def SaveBill(self):
        self.bill = { "name":self.name, "total":self.total, "due": self.date}