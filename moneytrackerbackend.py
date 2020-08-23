import csv
import os.path
import random
import string
from os import path
from datetime import date

#2019, 2023, 2027 - leap years

monthsNonLeap = [
    {"January": 31},
    {"February": 28},
    {"March": 31},
    {"April": 30},
    {"May": 31},
    {"June": 30},
    {"July": 31},
    {"August": 31},
    {"September": 30},
    {"October": 31},
    {"November": 30},
    {"December": 30}
]

monthsNonLeap = [
    {"January": 31},
    {"February": 29},
    {"March": 31},
    {"April": 30},
    {"May": 31},
    {"June": 30},
    {"July": 31},
    {"August": 31},
    {"September": 30},
    {"October": 31},
    {"November": 30},
    {"December": 30}
]

class MoneyTracker:
    #def __init__(self, payCheckAmount):
    #    self.payCheckDate = '03-06'
    #    self.payCheckAmount = payCheckAmount
    
    #write functions
    def transaction(self, transaction_type, transaction_amount):

        chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
        ID = ''.join(random.choice(chars) for length in range(10))

        print(ID)

        if path.isfile('transactions.csv'):
            with open('transactions.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow([transaction_type, transaction_amount, str(date.today())[5:10], ID])
        
        else:
            with open('transactions.csv', 'w') as csvfile:
                fieldnames = ['Type', 'Amount', 'Date', 'ID']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

                writer.writeheader()
                writer.writerow({'Type' : transaction_type, 'Amount' : transaction_amount, 'Date' : str(date.today())[5:10], 'ID' : ID})

    def writeFinancesCSV(self, payCheckDate, payCheckAmount, amountSave):

        chars=string.ascii_uppercase + string.digits + string.ascii_lowercase
        ID = ''.join(random.choice(chars) for length in range(10))

        print(ID)

        if path.isfile('finances.csv'):
            with open('finances.csv', 'a') as csvfile:
                writer = csv.writer(csvfile)

                writer.writerow([payCheckDate, payCheckAmount, amountSave, ID])
        
        #grab the current amount amount from database
        else:

            with open('finances.csv', 'w') as csvfile:
                fieldnames = ['PaycheckDate', 'PaycheckAmount', 'Save', 'ID']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                writer.writerow({'PaycheckDate' : payCheckDate, 'PaycheckAmount' : payCheckAmount, 'Save' : amountSave, 'ID' : ID})

    #read functions
    def readTransactionsCSV(self):
        with open('transactions.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            rowData = []
            for row in reader:
                rowData.append(row)

        return rowData

    
    def readFinancesCSV(self):

        with open('finances.csv') as csvfile:
            reader = csv.DictReader(csvfile)

            rowData = []
            for row in reader:
                rowData.append(row)

        return rowData
    
    def delete(self):
        pass


    def currentTotals(self):
        #total amounts in finance
        total_paycheck = 0
        total_to_save = 0

        #total amounts in transactions
        total_transaction = 0

        #total after save amount and transactions
        amount_to_spend = 0

        for rowFinances in self.readFinancesCSV():
            print(rowFinances)
            total_paycheck += float(rowFinances['PaycheckAmount'])
            total_to_save += float(rowFinances['Save'])
        
        for rowTransactions in self.readTransactionsCSV():
            total_transaction += float(rowTransactions['Amount'])

        current_amount = total_paycheck - total_transaction
        amount_to_spend = total_paycheck - total_to_save - total_transaction

        #format it to only go to tenth place, i dont care about adding trailing zeros so eh
        total_paycheck = round(total_paycheck,2)
        total_to_save = round(total_to_save,2)
        current_amount = round(current_amount,2)
        amount_to_spend = round(amount_to_spend,2)
        
        calculation = {
            "TotalAmount" : total_paycheck, 
            "TotalToSave" : total_to_save, 
            "TotalTransactions" : total_transaction,
            "AmountToSpend" : amount_to_spend,
            "CurrentAmount" : current_amount
        }
        return calculation
"""
###maybe use this for later, idk too much work rn to format stuff lol###
    def formatMoney(self, paycheck_amount, amount_to_save_for_pay_period):
        if '.' not in paycheck_amount:
            paycheck_amount = paycheck_amount + '.0'
            
        if '.' not in amount_to_save_for_pay_period:
            amount_to_save_for_pay_period = amount_to_save_for_pay_period + '.0'
                
        afterDecimal = amount_to_save_for_pay_period.split('.')
        #check paycheck_amount
        while len(afterDecimal[1]) < 2:
            paycheck_amount = paycheck_amount + '0'
            afterDecimal = paycheck_amount.split('.')

        #check amount_to_save
        afterDecimal = amount_to_save_for_pay_period.split('.')
        while len(afterDecimal[1]) < 2:
            amount_to_save_for_pay_period = amount_to_save_for_pay_period + '0'
            afterDecimal = paycheck_amount.split('.')

        print(paycheck_amount)
        print(amount_to_save_for_pay_period)
"""
test = MoneyTracker()
print(test.readFinancesCSV())
print(test.currentTotals())

"""
############################################################################################
############################################################################################
############################################################################################
## The bottom is for time purposes and keeping track of bi-weekly paychecks ##
############################################################################################
############################################################################################

    def currentPeriod(self):
        today = date.today()
        dayAndMonth = str(today)[5:10]
        with open('finances.csv') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                latestPayCheck = str(row['Paycheck Date'])

        todayDay = int(dayAndMonth[3:5])

        monthOfPaycheck = int(latestPayCheck[0:2])
        dayOfPaycheck = int(latestPayCheck[3:5])

        print(today)

        #31 because thats the highest number a day can go in a month
        #paycheck is biweekly so we use 14


        #this is wrong tho
        #must account for each month 
        #ex: current period is true with this ----- 31 (March) 1,2,3 (April) > 03 (todays date=April 03) > 20 (pay check date)
        if ((dayOfPaycheck + 14 > todayDay > dayOfPaycheck) and ((dayOfPaycheck+14) < 31)):
            print('current pay period')
            return True
        else:
            print('next pay period')
            return False
    
    def checkMonth(self, dayOfPaycheck, monthOfPaycheck):
        today = str(date.today()[5:10])
        month = str(today[0:2])
        day = str(today[3:5])

        #First Half (Day = 0 - 14) - Lowest amnt of days in a month is 28 and biweekly is 14 so 14+14 = 28
        if day <= 14 and month == monthOfPaycheck:
            if dayOfPaycheck+14 > day > dayOfPaycheck:
                return True
            else:
                return False

        #Second Half (Day = 15+) - Trickier, we must go off of last paycheck date
        elif day > 14 and month == monthOfPaycheck:
            if monthsNonLeap[month+1] > day > dayOfPaycheck:
                return True
            
        elif day >=14 and month+1 == monthOfPaycheck:
            pass

    #This function will loop until it finds the correct paycheck period based on the day and last paycheck Date
    def updatePayCheck(self, dayOfPaycheck, monthOfPaycheck, yearOfPaycheck):
        today = int(date.today()[5:10])
        month = int(today[0:2])
        day = int(today[3:5])
        daysInRangeNextMonth = 0

        #check if the paycheck day exceeds the number of months
        if dayOfPaycheck > (monthsNonLeap[monthOfPaycheck+1]):
            dayInRangeNextMonth = dayOfPaycheck - monthsNonLeap[monthOfPaycheck+1]

        #do operations if monthOfPaycheck is less than current month 
        if (not month >= monthOfPaycheck) or ((not dayOfPaycheck+14> today > dayOfPaycheck) or (not )):

            while (month != monthOfPaycheck) and (today > dayOfPaycheck):
                dayOfPaycheck += 14

                if (dayOfPaycheck > monthsNonLeap[monthOfPaycheck+1]):
                    dayOfPaycheck = dayOfPaycheck - monthsNonLeap[monthOfPaycheck-1]
                    monthOfPaycheck += 1


        
        else:
"""
        

    
