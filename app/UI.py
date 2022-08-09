
import os
import tkinter
import json
from tkinter import Scrollbar, StringVar, messagebox
from tkinter.font import BOLD
from app.bill import bill
from app.calculate import calculate
from app.balance import balance

class GUI:
    def __init__(self):

        self.bills = []
        self.bill_checkboxes = []
        self.selected_bills = []
        self.balance = balance(0)

        self.rows = 1

        self.mainWindow = tkinter.Tk() #Main Window
        self.mainWindow.title("Bill Pay") #Title

        self.SetGeometry(500,500, self.mainWindow)
        
        self.mainWindow.grid_columnconfigure((0,8), weight=1)

        self.DrawBalance()

        self.LoadFile()
        self.DrawButtons()

        self.mainWindow.mainloop()
    
    def SetGeometry(self, width, height, window):
        window_width = width
        window_height = height

        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()

        center_x = int(screen_width/2 - window_width / 2)
        center_y = int(screen_height/2 - window_height / 2)

        window.geometry('{}x{}+{}+{}'.format(window_width, window_height, center_x, center_y))

    def AddBillFrame(self, __bill):
        
        self.rows+=1 

        bill_Frame = tkinter.Frame()
        bill_Frame.grid(
            row = self.rows, 
            column=1, 
            columnspan=7,
            pady=15)

        bill_name_label = tkinter.Label(
            bill_Frame, 
            text = "{}:".format(__bill.name), 
            font=("Arial", 20, BOLD))

        bill_name_label.grid(
            row = self.rows, 
            column=2,
            sticky="sw")

        bill_amount_label = tkinter.Label(
            bill_Frame, 
            text ="${}".format(__bill.total), 
            font=("Arial", 20))

        bill_amount_label.grid(
            row = self.rows, 
            column=3,
            sticky="s")

        bill_date_label = tkinter.Label(
            bill_Frame, 
            text = "Due: {}".format(__bill.date), 
            font=("Arial", 20))

        bill_date_label.grid(
            row = self.rows, 
            column=4,
            sticky="s")

        bill_pay_checkValue = tkinter.IntVar()
        self.bill_checkboxes.append(bill_pay_checkValue)
        index = len(self.bill_checkboxes)-1

        bill_pay_checkbox = tkinter.Checkbutton(
            bill_Frame, 
            text="Pay",
            font=("Arial", 15),
            variable=bill_pay_checkValue,
            onvalue=1,
            offvalue=0,
            command=lambda: self.CheckValue(self.bill_checkboxes[index], index))

        bill_pay_checkbox.grid(
            row = self.rows, 
            column=5, 
            columnspan=2,
            sticky="s")

        bill_remove_button = tkinter.Button(
            bill_Frame,
            text="Remove",
            command=lambda: self.RemoveEntry(index, bill_Frame)
        )
        
        bill_remove_button.config(width=4)

        bill_remove_button.grid(
            row=self.rows,
            column=7,
            sticky="se"
        )
        
    def CheckValue(self, checkbox, index):
        if checkbox.get():
            self.selected_bills.append(self.bills[index])
        else:
            for entry in self.selected_bills:
                if entry == self.bills[index]:
                    self.selected_bills.remove(entry)

    def DrawBillInfo(self):
        self.billWindow = tkinter.Tk()
        self.billWindow.title("New Bill")
        self.SetGeometry(300,150, self.billWindow)
        
        self.name_frame = tkinter.Frame(self.billWindow)
        self.name_frame.pack(pady=5)
        self.name_label = tkinter.Label(self.name_frame, text="Name: ")
        self.name_label.pack(side="left")
        self.name_input = tkinter.Text(self.name_frame, height=1, width = 20)
        self.name_input.pack(side="left")

        self.date_frame = tkinter.Frame(self.billWindow)
        self.date_frame.pack(pady=5)
        self.date_label = tkinter.Label(self.date_frame, text="Due: ")
        self.date_label.pack(side="left")
        self.date_input = tkinter.Text(self.date_frame, height=1, width = 20)
        self.date_input.pack(side="left")

        self.amt_frame = tkinter.Frame(self.billWindow)
        self.amt_frame.pack(pady=5)
        self.amt_label = tkinter.Label(self.amt_frame, text="Amount: ")
        self.amt_label.pack(side="left")
        self.amt_input = tkinter.Text(self.amt_frame, height=1, width = 20)
        self.amt_input.pack(side="left")

        self.add_buttn = tkinter.Button(self.billWindow, text="Add", command=self.GetBillInfo)
        self.add_buttn.pack()

    def GetBillInfo(self):
        name = self.name_input.get(1.0, tkinter.END + "-1c")
        date = self.date_input.get(1.0, tkinter.END + "-1c")
        amt = self.amt_input.get(1.0, tkinter.END + "-1c")
        newBill = bill(name, amt, date)
        newBill.SaveBill()
        print("Added Bill to Dict")
        self.bills.append(newBill.bill)
        print("Added Bill to List")
        self.AddBillFrame(newBill)
        self.billWindow.destroy()
        self.DrawButtons()
    
    def DrawButtons(self):
        try:
            if self.new_bill_button.winfo_exists():
                self.new_bill_button.grid_remove()
            if self.save_button.winfo_exists():
                self.save_button.grid_remove()
            if self.calc_button.winfo_exists():
                self.calc_button.grid_remove()
            if self.exit_button.winfo_exists():
                self.exit_button.grid_remove()
        except:
            pass
    
        currentRow = int(self.rows) + 1

        self.button_frame = tkinter.Frame()
        self.button_frame.grid(
            row=currentRow,
            column=1,
            columnspan=7
        )

        self.new_bill_button = tkinter.Button(
            self.button_frame, 
            text="New Bill", 
            command=self.DrawBillInfo)

        self.new_bill_button.grid(
            pady=15, 
            row=currentRow, 
            column=1, 
            columnspan=2,
            sticky="ew")

        self.save_button = tkinter.Button(
            self.button_frame, 
            text="Save", 
            command=self.SaveBills)

        self.save_button.grid(
            pady=15,
            row=currentRow, 
            column=3, 
            columnspan=2,
            sticky="ew") 
        self.save_button.config(width=5)

        self.calc_button = tkinter.Button(
            self.button_frame, 
            text="Calculate", 
            command=self.CalculateBills)

        self.calc_button.grid(
            pady=15,
            row=currentRow, 
            column=5, 
            columnspan=2,
            sticky="ew") 
        self.calc_button.config(width=5)

        self.exit_button = tkinter.Button(
            self.button_frame, 
            text="Exit", 
            command=lambda: self.Exit())

        self.exit_button.grid(
            pady=5,
            row=currentRow, 
            column=7, 
            columnspan=2,
            sticky="ew") 
        self.exit_button.config(width=5)

    def DrawBalance(self):
        self.income_frame = tkinter.Frame()
        self.income_frame.grid(
            pady=10,
            padx=20,
            row=0,
            column=1,
            columnspan=6)

        self.income_label = tkinter.Label(
            self.income_frame, 
            text="Paycheck $",
            font=("Arial", 20))
        self.income_label.grid(
            row=0, 
            column=3)

        self.income_input = tkinter.Text(
            self.income_frame, 
            width=5, 
            height=1,
            font=("Arial", 20))

        self.income_input.grid(
            row=0, 
            column=4)

        self.remaining_balance_frame = tkinter.Frame()
        self.remaining_balance_frame.grid(
            pady=10,
            row=1,
            column=1,
            columnspan=6)

        self.remaining_balance_label = tkinter.Label(
            self.remaining_balance_frame,
            text="Remaining: $",
            font=("Arial", 20, BOLD)
        )

        self.remaining_balance_label.grid(
            row=1,
            column=0,
            sticky="sw"
        )

        self.remaining_balance_value = StringVar()
        self.remaining_balance_value.set(self.balance.GetTotal())

        self.remaining_balance_value_label = tkinter.Label(
            self.remaining_balance_frame,
            textvariable=self.remaining_balance_value,
            font=("Arial", 20)
        )

        self.remaining_balance_value_label.grid(
            row = 1,
            column=1,
            sticky="sw"
        )

    def CheckFiles(self):
        mainDir = os.getcwd()
        newDir = mainDir + "/bills"

        if not os.path.exists(newDir):
            print("No Saved Files")
            return False
        else:
            return True

    def SaveBills(self):
        if tkinter.messagebox.askyesno("Save", "Would you like to save?"):
            try:
                mainDir = os.getcwd()
                newDir = mainDir + "/bills"
                if not os.path.exists(newDir):
                    os.makedirs(newDir)
                    print("Directory Added")
            except IOError:
                tkinter.messagebox.showerror("Error","Unable to Create Directory")
            else:
                #for bill in self.bills:
                json_file = json.dumps(self.bills, indent=4)
                
                with open(os.path.join(newDir, "bill.json"), "w") as outfile:
                    outfile.write(json_file)
        
            print("File Saved")

    def LoadFile(self):
        if self.CheckFiles():
            mainDir = os.getcwd()
            fileDir = mainDir + "/bills"
            with open(fileDir+"/bill.json", "r") as f:
                self.bills = json.load(f)
            for entry in self.bills:
                name = entry.get("name")
                amt = entry.get("total")
                date = entry.get("due")
                newBill = bill(name,amt,date)
                self.AddBillFrame(newBill)

    def CalculateBills(self):
        calc = calculate()
        try:
            if len(self.income_input.get(1.0, tkinter.END + "-1c")) == 0:
                raise ValueError
            else:
                income = self.income_input.get(1.0, tkinter.END + "-1c")
                self.balance.SetTotal(income)

            for bills in self.selected_bills:
                calc.PayBill(self.balance, bills)

            self.remaining_balance_value.set(self.balance.GetTotal())

        except ValueError:
            tkinter.messagebox.showerror("Error", "No Income Added")

    def RemoveEntry(self,index,frame):
        if tkinter.messagebox.askokcancel("Remove Bill", "Are you sure you want to delete this?"):
            try:
                for entry in self.selected_bills:
                    if entry == self.bills[index]:
                        self.selected_bills.remove(entry)
                print(self.selected_bills)
                self.bills.pop(index)
                self.bill_checkboxes.pop(index)
            except IndexError:
                self.bills.clear()
                self.bill_checkboxes.clear()
                for widget in frame.winfo_children():
                    widget.destroy()
                frame.destroy()       
            else:
                for widget in frame.winfo_children():
                    widget.destroy()
                frame.destroy()                
                
    def Exit(self):
        if tkinter.messagebox.askyesno("Exit", "Are you sure you want to exit?"):
            self.mainWindow.destroy()