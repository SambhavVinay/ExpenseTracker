from flask import Flask, redirect, request, render_template
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
all = []
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Expenses.db'
db = SQLAlchemy(app)

class Expenses(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(100), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date_added = db.Column(db.Date, default=datetime.utcnow)

def __repr__(self):
    return f"<{self.title}:{self.amount} on {self.date_added}>"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/add_expense",methods=["POST","GET"])
def add_expense():
    global all
    if request.method == "POST":
        TITLE = request.form["TITLE"]
        AMOUNT = request.form["AMOUNT"]

        new_expense = Expenses(
            title = TITLE,
            amount = AMOUNT
        )
        try:
            db.session.add(new_expense)
            db.session.commit()
        except:
            return "Failed to add Record!!"
        return redirect("/display")
    return render_template("add_expense.html")

@app.route("/delete/<int:id>")
def delete(id):
    delete_expense = Expenses.query.get_or_404(id)
    try:
        db.session.delete(delete_expense)
        db.session.commit()
    except:
        return "Failed to Remove Record!!"
    return redirect("/display")

@app.route("/update/<int:id>",methods = ["POST","GET"])
def update(id):
 updated_expense = Expenses.query.get_or_404(id)
 if request.method == "POST":
    updated_expense.title = request.form["TITLE"]
    updated_expense.amount = request.form["AMOUNT"]
    try:
        db.session.commit()
        return redirect("/display")
    except:
        return "Failed to Update Record!!"
 return render_template("update.html",updated_expense = updated_expense)
    

@app.route("/display")
def display():
    global all
    display_expenses = Expenses.query.order_by(Expenses.date_added).all()
    return render_template("display.html",display_expenses = display_expenses)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)