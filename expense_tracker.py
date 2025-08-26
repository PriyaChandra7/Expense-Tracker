#import libraries 
import matplotlib.pyplot as plt  #for creatin graph
import json #for save and load file
from datetime import datetime
from collections import defaultdict #for grouping

expenses=[]

def load_expenses():
    try:
        with open("expenses.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return[ ]

#load saved expenses at starting if present
expenses = load_expenses() 

def add_expense():
    while True:
        expense=input("Expense Type: ")
        amt=float(input("Enter the amount: "))
        #ask user for a date, default:today's date
        dateInput= input("Enter date ( YYYY-MM-DD) or press Enter for today: ")
        if dateInput.strip() == "":
            dateValue= datetime.today().strftime('%Y-%m-%d')
        else:
            dateValue = dateInput
            
        dic={"date": dateValue, "name": expense, "amount": amt}
        expenses.append(dic)  #add dictionary to the list
        print("Expense added successfully :)")

        more= input("Add another expense? (y/n): ")
        if more.lower() != 'y':
            break

def view_expense():
    if len(expenses) == 0:
        print("No expenses found")
        return

    #show all individual expenses
    print("\nAll Expenses: ")
    for index, expense in enumerate(expenses, start=1):
        print(f"{index}. Expense Type: {expense['name']} | Amount: {expense['amount']} | Date: {expense['date']}")

    #dictionaries to store grouped total
    daily_summary = defaultdict(float)
    weekly_summary = defaultdict(float)
    monthly_summary = defaultdict(float)
    
    for exp in expenses:
        date_obj = datetime.strptime(exp['date'], '%Y-%m-%d')

        #daily summary
        daily_summary[date_obj.date()] += exp['amount']

        #weekly summary. (ISO calender: year+week no.)
        year, week_num, _ = date_obj.isocalendar()
        weekly_summary[f"{year}-W{week_num}"] += exp['amount']

        #monthly summary(year, month format)
        month_key = f"{date_obj.year}-{date_obj.month:02d}"
        monthly_summary[month_key] += exp['amount']

    print("\nDaily Spending Summary:")
    for date, total in daily_summary.items():
        print(f"{date}: {total}")

    print("\nWeekly Spending Summary:")
    for week, total in weekly_summary.items():
        print(f"{week}: {total}")

    print("\nMonthly Spending Summary:")
    for month, total in monthly_summary.items():
        print(f"{month}: {total}")
        

#display whole amount spent         
def calculate_total():
    if len(expenses)==0:
        print("No expenses found")
    else:
        total=0
        for expense in expenses:
            total=total+expense['amount']
        print(f"Total expense: {total}")

#save expense to file
def save_expenses():
    with open("expenses.json", "w") as file:
        json.dump(expenses, file, indent=4)


#edit existing expense
def edit_expenses():
    while True:
        view_expense()
        try:
            ix= int(input("Enter the index of expense which you want to edit"))
            if (0<= ix<len(expenses)):
                edit=input("What you want to edit (name, amount,both): ")
                
                if edit.lower() == "name":
                    expenses[ix]['name']= input("Enter new expense name: ")
                    print("Expense-Type is updated")
                elif edit.lower() == "amount":
                    expenses[ix]['amount']= float(input("Enter new amount: "))
                    print("Amount is updated!")
                elif edit.lower() == "both":
                    expenses[ix]['name']= input("Enter new expense name: ")
                    expenses[ix]['amount']= float(input("Enter new amount: "))
                    print("Updated Successfully")
                else:
                    print("Invalid choice for edit")
            else:
                print("Invalid index!")
        except ValueError:
            print("Please enter a valid number!")
        more= input("Want to edit more expense (y/n): ")
        if more.lower()!= 'y':
            break

#delete an expense
def del_expenses():
    while True:
        view_expense()
        try:
            indx = int(input("Enter the index of expense you want to delete: "))
            if ( 0<= indx < len(expenses)):
                expenses.pop(indx)
                print("Deletion Sucessfull!")
            else:
                print("Invalid Index")
        except ValueError:
            print("Please enter a valid number")
            
        more= input("Want to delete more expense (y/n): ")
        if more.lower()!= 'y':
            break;
 #show pi chart
def show_summary():
    if not expenses:
        print("No expense to show!")
        return
    
    categories = [expense['name'] for expense in expenses]
    amounts= [expense['amount'] for expense in expenses]

    plt.figure(figsize=(6,6))
    plt.pie(amounts, labels=categories, autopct='%1.1f%%', startangle=140)
    plt.title("Expense Distribution")
    plt.show()

#main menu
def main(): 
    while True:
        print("\n=== Personal Expense Tracker ===")
        print("1. Add Expense")
        print("2. View Summary")
        print("3. View Total Expense")
        print("4. Edit an Expense")
        print("5. Delete an Expense")
        print("6. Show Expense Summary(Graph)")
        print("7. Exit")
        
        choice= input("Enter your choice: ")

        if choice == "1":
            add_expense()
            save_expenses()
        elif choice == "2":
            view_expense()
        elif choice == "3":
            calculate_total()
        elif choice == "4":
            edit_expenses()
        elif choice == "5":
            del_expenses()
        elif choice == "6":
            show_summary()
        elif choice == "7":
            save_expenses()
            print("Exiting...Goodbye!")
            break
        else:
            print("Invalid choice, try again.")
#run the main program
if __name__ == "__main__":
    main()

