class calculate:
    def __init__(self) -> None:
         pass

    def PayBill(self, balance, bill):
        newBalance = int(balance.GetTotal()) - int(bill.get("total"))
        balance.SetTotal(newBalance)
        #__newBalance = balance.CalculatePayment(bill)
        #balance.SetTotal(__newBalance)

    def PrintBalance(self, currentBalance):
        print("$" + str(currentBalance.GetTotal()))
