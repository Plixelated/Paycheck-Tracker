import os
import tkinter
from tkinter import ttk
import json
from tkinter import Scrollbar, StringVar, messagebox
from tkinter.font import BOLD
from tkinter.tix import COLUMN
from app.ScrollableFrame import ScrollableFrame 
from app.bill import bill
from app.calculate import calculate
from app.balance import balance

class GUI:
    def __init__(self):

        self.bills = []
        self.bill_checkboxes = []
        self.selected_bills = []
        self.bill_frames = []
        self.balance = balance(0)


        self.rows = 1

        self.root = tkinter.Tk() #Main Window
        self.root.title("Bill Pay") #Title

        self.SetGeometry(700,400, self.root)
        
        self.root.grid_columnconfigure((0,8), weight=1)

        self.scrollField = ScrollableFrame(self.root)
        self.scrollField.grid(row=2, column=4, columnspan=5, sticky="nesw")
        

        self.DrawBalance()

        self.LoadFile()
        self.DrawButtons()

        self.root.mainloop()
    
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
        total = __bill.total
        total = "${:0,.2f}".format(float(total))

        bill_Frame = tkinter.Frame(self.scrollField.scrollable_frame)
        bill_Frame.grid(
            row = self.rows,
            sticky="ew",
            pady=15
        )

        bill_name_label = tkinter.Label(
            bill_Frame, 
            text = "{}:".format(__bill.name), 
            font=("Arial", 20, BOLD)
            )

        bill_name_label.grid(
            row = self.rows, 
            column=2,
            sticky="s")

        bill_amount_label = tkinter.Label(
            bill_Frame, 
            text ="{}".format(total), 
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
            command=lambda: self.Calculate(index))#self.CheckValue(self.bill_checkboxes[index], index))

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
            sticky="s"
        )

        '''children_widgets = bill_Frame.winfo_children()
        for child_widget in children_widgets:
            if child_widget.winfo_class() == 'Label':
                print(child_widget.cget("text"))'''

    #DEPRECATED
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
        amt = amt.replace("$","")
        amt = amt.replace(",","")
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
    
        #currentRow = int(self.rows) + 1
        currentRow = 5

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

        '''self.calc_button = tkinter.Button(
            self.button_frame, 
            text="Calculate", 
            command=self.CalculateBills)

        self.calc_button.grid(
            pady=15,
            row=currentRow, 
            column=5, 
            columnspan=2,
            sticky="ew") 
        self.calc_button.config(width=5)'''

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
            width=8, 
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

        self.submit_balance_btn = tkinter.Button(
            self.income_frame,
            text="Set",
            command=lambda: self.AddBalance())
        
        self.submit_balance_btn.grid(
            row = 0,
            column=5,
            columnspan=2
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
    #DEPRECATED
    def CalculateBills(self):
        calc = calculate()
        try:
            if len(self.selected_bills) < 1:
                raise ValueError
            else:
                for bills in self.selected_bills:
                    calc.PayBill(self.balance, bills)

            self.remaining_balance_value.set(self.balance.GetTotal())

        except ValueError:
            tkinter.messagebox.showerror("Error", "No Bills Selected")

    def Calculate(self, index):
        try:
            if self.balance.GetTotal() == 0 and len(self.income_input.get(1.0, tkinter.END + "-1c")) == 0:
                raise ValueError
            else:
                if self.bill_checkboxes[index].get():
                    total = float(self.balance.GetTotal()) - float(self.bills[index].get("total"))
                    total = "{:0,.2f}".format(total)
                else:
                    total = float(self.balance.GetTotal()) + float(self.bills[index].get("total"))
                    total = "{:0,.2f}".format(total)
            
                self.balance.SetTotal(total)
                self.remaining_balance_value.set(self.balance.GetTotal())

        except ValueError:
            tkinter.messagebox.showerror("Error", "No Income Added")
        except IndexError:
            tkinter.messagebox.showerror("Error", "List index: {} out of range".format(index))

    def AddBalance(self):
        try:
            if len(self.income_input.get(1.0, tkinter.END + "-1c")) == 0:
                raise ValueError
            else:
                income = self.income_input.get(1.0, tkinter.END + "-1c")
                income = income.replace(",","")
                self.balance.SetTotal(income)

                income_formatted = "{:0,.2f}".format(float(self.balance.GetTotal()))
                self.remaining_balance_value.set(income_formatted)

                self.income_input.delete("1.0","end")

        except ValueError:
            tkinter.messagebox.showerror("Error", "No Income Added")
            
    def RemoveEntry(self,index,frame):
        if tkinter.messagebox.askokcancel("Remove Bill", "Are you sure you want to delete this?"):
            try:
                '''for entry in self.selected_bills:
                    if entry == self.bills[index]:
                        self.selected_bills.remove(entry)
                print(self.selected_bills)'''
                
                for entry in self.bill_checkboxes:
                    if entry.get():
                        total = float(self.balance.GetTotal()) + float(self.bills[index].get("total"))
                        total = "{:0,.2f}".format(total)
                        self.balance.SetTotal(total)
                        self.remaining_balance_value.set(self.balance.GetTotal())

                self.bills.pop(index)
                #self.bill_checkboxes.pop(index)

                for child in self.scrollField.scrollable_frame.winfo_children():
                    child.destroy()
                self.bill_checkboxes.clear()
                for entry in self.bills:
                    name = entry.get("name")
                    amt = entry.get("total")
                    date = entry.get("due")
                    newBill = bill(name,amt,date)
                    self.AddBillFrame(newBill)

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
            self.root.destroy()