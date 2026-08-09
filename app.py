from flask import Flask, render_template, request, redirect
from pymongo import MongoClient
from config import Config
from datetime import datetime


app = Flask(__name__)


# MongoDB Connection
client = MongoClient(Config.MONGO_URI)

db = client["expenseDB"]

expenses_collection = db["expenses"]



# Home page - Display all expenses
@app.route("/")
def home():

    expenses = expenses_collection.find()

    return render_template(
        "index.html",
        expenses=expenses
    )



# Add expense page
@app.route("/add")
def add_expense_page():

    return render_template(
        "add_expense.html"
    )



# Save expense into MongoDB
@app.route("/add_expense", methods=["POST"])
def add_expense():

    expense = {

        "title": request.form["title"],

        "amount": int(request.form["amount"]),

        "category": request.form["category"],

        "payment": request.form["payment"],

        "date": datetime.now().strftime("%Y-%m-%d")

    }


    expenses_collection.insert_one(expense)


    return redirect("/")



# Dashboard page
@app.route("/dashboard")
def dashboard():

    result = expenses_collection.aggregate(
        [
            {
                "$group":
                {
                    "_id": "$category",
                    "total":
                    {
                        "$sum": "$amount"
                    }
                }
            }
        ]
    )


    return render_template(
        "dashboard.html",
        data=result
    )



if __name__ == "__main__":
    app.run(debug=True)