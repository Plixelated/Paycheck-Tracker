class calculate:
    def __init__(self):
         pass

    def PayBill(self, balance, bill):
        newBalance = float(balance.GetTotal()) - float(bill.get("total"))
        balance.SetTotal(newBalance)
        #__newBalance = balance.CalculatePayment(bill)
        #balance.SetTotal(__newBalance)

    def PrintBalance(self, currentBalance):
        print("$" + str(currentBalance.GetTotal()))
