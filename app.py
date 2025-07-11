from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Ensure database exists before using it
if not os.path.exists('expenses.db'):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS expenses 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, date TEXT, category TEXT, amount REAL, note TEXT)''')
    conn.commit()
    conn.close()

@app.route('/', methods=['GET', 'POST'])
def index():
    error = None
    if request.method == 'POST':
        date = request.form['date']
        category = request.form['category']
        amount = request.form['amount']
        note = request.form['note']

        # Validation logic
        if not date or not category or not amount:
            error = "⚠️ Please fill in all required fields."
        elif float(amount) <= 0:
            error = "⚠️ Amount must be greater than ₹0."
        else:
            conn = sqlite3.connect('expenses.db')
            cursor = conn.cursor()
            cursor.execute("INSERT INTO expenses (date, category, amount, note) VALUES (?, ?, ?, ?)",
                           (date, category, amount, note))
            conn.commit()
            conn.close()
            return redirect('/expenses')

    return render_template('index.html', error=error)

@app.route('/expenses')
def view_expenses():
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM expenses")
    expenses = cursor.fetchall()
    conn.close()
    return render_template('expenses.html', expenses=expenses)

@app.route('/delete/<int:id>')
def delete_expense(id):
    conn = sqlite3.connect('expenses.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM expenses WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect('/expenses')

if __name__ == '__main__':
    app.run(debug=True)