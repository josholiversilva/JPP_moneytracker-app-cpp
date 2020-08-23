"""  Money Tracker   """

from flask import Flask
from flask import request, redirect, url_for, render_template, flash
from datetime import date
import os
from moneytrackerbackend import MoneyTracker

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

port = int(os.environ.get('PORT',5000))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        password = request.form['password']
        print(user)
        print(password)
    
        if user == 'admin' and password == 'password':
            print('LOGGED IN')
            return redirect(url_for('main_transactions'))

        else:
            print('ERROR')
            return render_template('index.html')

@app.route('/main_transactions', methods = ['GET', 'POST'])
def main_transactions():

    if request.method == 'POST':
        transaction = request.form.get('transaction','')
        transaction_type = request.form.get('type','')
        goFinances = request.form.get('goFinances', '')

        if goFinances != '':
            return redirect(url_for('main_finances'))
    
        elif transaction!='' and transaction_type!= '' and goFinances == '':
            MoneyTracker().transaction(transaction_type, transaction)
            return render_template(
                    'main.html', 
                    finances=MoneyTracker().readFinancesCSV(), 
                    transactions=MoneyTracker().readTransactionsCSV(),
                    totals=MoneyTracker().currentTotals()
                )

        else:
            flash('Looks like you did NOT input both!')
            return render_template(
                'main.html', 
                finances=MoneyTracker().readFinancesCSV(), 
                transactions=MoneyTracker().readTransactionsCSV(),
                totals=MoneyTracker().currentTotals()
            )

    else:
        return render_template(
            'main.html', 
            finances=MoneyTracker().readFinancesCSV(), 
            transactions=MoneyTracker().readTransactionsCSV(),
            totals=MoneyTracker().currentTotals()
        )


@app.route('/main_finances', methods = ['GET', 'POST'])
def main_finances():

    if request.method == 'POST':
        paycheck_amount = request.form.get('paycheck_amount','')
        paycheck_date = request.form.get('paycheck_date','')
        amount_to_save_for_pay_period = request.form.get('amount_save','')

        goTransactions = request.form.get('goTransactions','')

        if goTransactions:
            return redirect(url_for('main_transactions'))

        elif paycheck_amount!='' and paycheck_date!='' and amount_to_save_for_pay_period!='' and goTransactions=='':

            MoneyTracker().writeFinancesCSV(paycheck_date, paycheck_amount, amount_to_save_for_pay_period)
            return render_template('main_finances.html', finances=MoneyTracker().readFinancesCSV(), totals=MoneyTracker().currentTotals())

        else:
            flash('Looks like you did NOT input ALL THREE!')
            return render_template('main_finances.html', finances=MoneyTracker().readFinancesCSV(), totals=MoneyTracker().currentTotals())

    else:
        return render_template('main_finances.html', finances=MoneyTracker().readFinancesCSV(), totals=MoneyTracker().currentTotals())

    def delete(self):
        deleteTransaction = request.form.get('deleteTransaction','')


if __name__ == "__main__":
    app.run(debug=False,host='0.0.0.0',port=port)

