
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
from datetime import datetime
from collections import defaultdict

app = Flask(__name__)

DATA_FILE = "expenses.json"


def load_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return {
                "expenses": data.get("expenses", []),
                "budget": float(data.get("budget", 0))
            }
        except (json.JSONDecodeError, OSError, ValueError):
            pass

    return {"expenses": [], "budget": 0}


def save_data(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)


@app.route("/")
def index():
    data = load_data()
    expenses = data["expenses"]
    budget = data["budget"]

    month = datetime.today().strftime("%Y-%m")
    monthly_total = sum(
        float(e.get("amount", 0))
        for e in expenses
        if str(e.get("date", "")).startswith(month)
    )

    total = sum(float(e.get("amount", 0)) for e in expenses)

    categories = defaultdict(float)
    for expense in expenses:
        categories[expense.get("category", "Other")] += float(
            expense.get("amount", 0)
        )

    months = []
    monthly_values = []

    today = datetime.today()
    for offset in range(5, -1, -1):
        month_number = today.month - offset
        year = today.year

        while month_number <= 0:
            month_number += 12
            year -= 1

        date = datetime(year, month_number, 1)
        key = date.strftime("%Y-%m")
        months.append(date.strftime("%b"))

        amount = sum(
            float(e.get("amount", 0))
            for e in expenses
            if str(e.get("date", "")).startswith(key)
        )
        monthly_values.append(amount)

    return render_template(
        "index.html",
        expenses=expenses,
        budget=budget,
        total=total,
        monthly_total=monthly_total,
        remaining=budget - monthly_total,
        categories=dict(categories),
        months=months,
        monthly_values=monthly_values
    )


@app.route("/add", methods=["POST"])
def add_expense():
    data = load_data()

    description = request.form.get("description", "").strip()
    category = request.form.get("category", "Other")
    amount_text = request.form.get("amount", "").strip()

    try:
        amount = float(amount_text)
        if amount <= 0 or not description:
            raise ValueError
    except ValueError:
        return redirect(url_for("index"))

    data["expenses"].append({
        "description": description,
        "category": category,
        "amount": amount,
        "date": datetime.today().strftime("%Y-%m-%d")
    })

    save_data(data)
    return redirect(url_for("index"))


@app.route("/delete/<int:index>", methods=["POST"])
def delete_expense(index):
    data = load_data()

    if 0 <= index < len(data["expenses"]):
        data["expenses"].pop(index)
        save_data(data)

    return redirect(url_for("index"))


@app.route("/budget", methods=["POST"])
def set_budget():
    data = load_data()

    try:
        budget = float(request.form.get("budget", ""))
        if budget <= 0:
            raise ValueError
        data["budget"] = budget
        save_data(data)
    except ValueError:
        pass

    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
