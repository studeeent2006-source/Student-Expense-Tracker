
import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import json
import os
from datetime import datetime
from collections import defaultdict

# ---------------- COLORS ----------------

BG = "#F4F5FA"
NAVY = "#202744"
PURPLE = "#7565D9"
WHITE = "#FFFFFF"
TEXT = "#252B42"
MUTED = "#858BA3"
GREEN = "#21A179"
RED = "#E45B68"
LIGHT_PURPLE = "#EAE7FF"

DATA_FILE = "expenses.json"


class ExpenseTracker:

    def __init__(self, root):
        self.root = root
        self.root.title("Student Expense Tracker")
        self.root.geometry("1100x720")
        self.root.minsize(950, 650)
        self.root.configure(bg=BG)

        self.expenses = []
        self.budget = 0.0

        self.load_data()
        self.setup_style()
        self.create_widgets()
        self.refresh_data()

    # ---------------- DATA ----------------

    def load_data(self):
        if not os.path.exists(DATA_FILE):
            return

        try:
            with open(DATA_FILE, "r", encoding="utf-8") as file:
                data = json.load(file)

            self.expenses = data.get("expenses", [])
            self.budget = float(data.get("budget", 0))

            # Support older expense records
            for expense in self.expenses:
                if "description" not in expense:
                    expense["description"] = expense.get(
                        "note", expense.get("title", "")
                    )
                if "amount" not in expense:
                    expense["amount"] = 0
                if "category" not in expense:
                    expense["category"] = "Other"
                if "date" not in expense:
                    expense["date"] = datetime.today().strftime("%Y-%m-%d")

        except (json.JSONDecodeError, OSError, TypeError, ValueError):
            messagebox.showerror(
                "Data Error",
                "Could not read expenses.json. Starting with empty data."
            )
            self.expenses = []
            self.budget = 0.0

    def save_data(self):
        data = {
            "expenses": self.expenses,
            "budget": self.budget
        }

        with open(DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    # ---------------- STYLING ----------------

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")

        style.configure(
            "Treeview",
            background=WHITE,
            foreground=TEXT,
            rowheight=34,
            fieldbackground=WHITE,
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#EAEAF3",
            foreground=NAVY,
            font=("Segoe UI", 10, "bold"),
            padding=8
        )

        style.map(
            "Treeview",
            background=[("selected", LIGHT_PURPLE)],
            foreground=[("selected", NAVY)]
        )

    # ---------------- MAIN UI ----------------

    def create_widgets(self):

        # Sidebar
        sidebar = tk.Frame(self.root, bg=NAVY, width=220)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(
            sidebar,
            text="STUDENT\nEXPENSE",
            bg=NAVY,
            fg=WHITE,
            font=("Segoe UI", 19, "bold"),
            justify="left"
        ).pack(anchor="w", padx=25, pady=(35, 8))

        tk.Label(
            sidebar,
            text="TRACKER",
            bg=NAVY,
            fg="#A99FFF",
            font=("Segoe UI", 10, "bold")
        ).pack(anchor="w", padx=27, pady=(0, 40))

        self.sidebar_button(sidebar, "Dashboard", self.refresh_data)
        self.sidebar_button(sidebar, "View Charts", self.show_charts)
        self.sidebar_button(sidebar, "Category Report", self.category_report)
        self.sidebar_button(sidebar, "Set Budget", self.set_budget)

        tk.Label(
            sidebar,
            text="Manage your money\nsmartly!",
            bg=NAVY,
            fg="#B8BED5",
            font=("Segoe UI", 10),
            justify="left"
        ).pack(side="bottom", anchor="w", padx=25, pady=25)

        # Main area
        self.main = tk.Frame(self.root, bg=BG)
        self.main.pack(side="left", fill="both", expand=True, padx=28, pady=24)

        header = tk.Frame(self.main, bg=BG)
        header.pack(fill="x", pady=(0, 22))

        tk.Label(
            header,
            text="Dashboard",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 24, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Track your daily expenses",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="right", pady=12)

        # Summary cards
        cards = tk.Frame(self.main, bg=BG)
        cards.pack(fill="x", pady=(0, 22))

        self.total_label = self.create_card(
            cards, "TOTAL EXPENSES", "₹0.00", PURPLE
        )
        self.budget_label = self.create_card(
            cards, "MONTHLY BUDGET", "₹0.00", GREEN
        )
        self.remaining_label = self.create_card(
            cards, "BUDGET LEFT", "₹0.00", RED
        )

        # Expense form
        form = tk.Frame(self.main, bg=WHITE, padx=18, pady=16)
        form.pack(fill="x", pady=(0, 20))

        tk.Label(
            form,
            text="Add New Expense",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 13))

        tk.Label(form, text="Description", bg=WHITE, fg=MUTED).grid(
            row=1, column=0, sticky="w"
        )
        tk.Label(form, text="Amount (₹)", bg=WHITE, fg=MUTED).grid(
            row=1, column=1, sticky="w"
        )
        tk.Label(form, text="Category", bg=WHITE, fg=MUTED).grid(
            row=1, column=2, sticky="w"
        )

        self.description_entry = tk.Entry(
            form, font=("Segoe UI", 10), relief="solid", bd=1
        )
        self.description_entry.grid(
            row=2, column=0, sticky="ew", padx=(0, 12), ipady=7
        )

        self.amount_entry = tk.Entry(
            form, font=("Segoe UI", 10), relief="solid", bd=1
        )
        self.amount_entry.grid(
            row=2, column=1, sticky="ew", padx=(0, 12), ipady=7
        )

        self.category_var = tk.StringVar(value="Food")
        self.category_combo = ttk.Combobox(
            form,
            textvariable=self.category_var,
            values=[
                "Food", "Travel", "Education", "Shopping",
                "Entertainment", "Bills", "Health", "Other"
            ],
            state="readonly",
            font=("Segoe UI", 10)
        )
        self.category_combo.grid(
            row=2, column=2, sticky="ew", padx=(0, 12), ipady=5
        )

        add_button = tk.Button(
            form,
            text="+ Add Expense",
            bg=PURPLE,
            fg=WHITE,
            activebackground="#6252C5",
            activeforeground=WHITE,
            font=("Segoe UI", 10, "bold"),
            relief="flat",
            cursor="hand2",
            command=self.add_expense
        )
        add_button.grid(row=2, column=3, sticky="ew", ipady=7)

        for column in range(4):
            form.grid_columnconfigure(column, weight=1)

        # Expense table
        table_frame = tk.Frame(self.main, bg=WHITE, padx=15, pady=15)
        table_frame.pack(fill="both", expand=True)

        tk.Label(
            table_frame,
            text="Recent Transactions",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", pady=(0, 12))

        columns = ("date", "description", "category", "amount")

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings",
            height=9
        )

        self.tree.heading("date", text="DATE")
        self.tree.heading("description", text="DESCRIPTION")
        self.tree.heading("category", text="CATEGORY")
        self.tree.heading("amount", text="AMOUNT")

        self.tree.column("date", width=120)
        self.tree.column("description", width=250)
        self.tree.column("category", width=150)
        self.tree.column("amount", width=130, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Bottom buttons
        bottom = tk.Frame(self.main, bg=BG)
        bottom.pack(fill="x", pady=15)

        self.action_button(
            bottom, "Delete Selected", RED, self.delete_expense
        ).pack(side="left", padx=(0, 10))

        self.action_button(
            bottom, "Refresh", NAVY, self.refresh_data
        ).pack(side="left", padx=5)

        self.action_button(
            bottom, "View Charts", PURPLE, self.show_charts
        ).pack(side="right")

    def sidebar_button(self, parent, text, command):
        button = tk.Button(
            parent,
            text="   " + text,
            command=command,
            bg=NAVY,
            fg=WHITE,
            activebackground="#343D61",
            activeforeground=WHITE,
            font=("Segoe UI", 11),
            relief="flat",
            anchor="w",
            cursor="hand2",
            padx=15,
            pady=12
        )
        button.pack(fill="x", padx=12, pady=4)

    def create_card(self, parent, title, value, color):
        card = tk.Frame(parent, bg=WHITE, padx=18, pady=16)
        card.pack(side="left", fill="both", expand=True, padx=(0, 12))

        tk.Label(
            card,
            text=title,
            bg=WHITE,
            fg=MUTED,
            font=("Segoe UI", 9, "bold")
        ).pack(anchor="w")

        label = tk.Label(
            card,
            text=value,
            bg=WHITE,
            fg=color,
            font=("Segoe UI", 19, "bold")
        )
        label.pack(anchor="w", pady=(7, 0))

        return label

    def action_button(self, parent, text, color, command):
        return tk.Button(
            parent,
            text=text,
            command=command,
            bg=color,
            fg=WHITE,
            activebackground=color,
            activeforeground=WHITE,
            relief="flat",
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            padx=16,
            pady=9
        )

    # ---------------- EXPENSE FUNCTIONS ----------------

    def add_expense(self):
        description = self.description_entry.get().strip()
        amount_text = self.amount_entry.get().strip()
        category = self.category_var.get()

        if not description or not amount_text:
            messagebox.showwarning(
                "Missing Information",
                "Please enter description and amount."
            )
            return

        try:
            amount = float(amount_text)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Invalid Amount",
                "Please enter a valid amount greater than zero."
            )
            return

        expense = {
            "date": datetime.today().strftime("%Y-%m-%d"),
            "description": description,
            "category": category,
            "amount": amount
        }

        self.expenses.append(expense)
        self.save_data()

        self.description_entry.delete(0, tk.END)
        self.amount_entry.delete(0, tk.END)

        self.refresh_data()
        messagebox.showinfo("Success", "Expense added successfully!")

    def refresh_data(self):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total = 0.0
        current_month = datetime.today().strftime("%Y-%m")

        for index, expense in enumerate(self.expenses):
            amount = float(expense.get("amount", 0))
            total += amount

            self.tree.insert(
                "",
                "end",
                iid=str(index),
                values=(
                    expense.get("date", ""),
                    expense.get("description", ""),
                    expense.get("category", ""),
                    f"₹{amount:,.2f}"
                )
            )

        monthly_total = sum(
            float(expense.get("amount", 0))
            for expense in self.expenses
            if str(expense.get("date", "")).startswith(current_month)
        )

        remaining = self.budget - monthly_total

        self.total_label.config(text=f"₹{total:,.2f}")
        self.budget_label.config(text=f"₹{self.budget:,.2f}")
        self.remaining_label.config(
            text=f"₹{remaining:,.2f}",
            fg=GREEN if remaining >= 0 else RED
        )

    def delete_expense(self):
        selected = self.tree.selection()

        if not selected:
            messagebox.showwarning(
                "No Selection",
                "Please select an expense to delete."
            )
            return

        if not messagebox.askyesno(
            "Confirm Delete",
            "Are you sure you want to delete the selected expense?"
        ):
            return

        indices = sorted(
            [int(item) for item in selected],
            reverse=True
        )

        for index in indices:
            if 0 <= index < len(self.expenses):
                self.expenses.pop(index)

        self.save_data()
        self.refresh_data()

    def set_budget(self):
        value = simpledialog.askfloat(
            "Set Monthly Budget",
            "Enter your monthly budget (₹):",
            minvalue=0.01,
            parent=self.root
        )

        if value is not None:
            self.budget = value
            self.save_data()
            self.refresh_data()
            messagebox.showinfo(
                "Budget Updated",
                f"Monthly budget set to ₹{value:,.2f}"
            )

    def category_report(self):
        totals = defaultdict(float)

        for expense in self.expenses:
            totals[expense.get("category", "Other")] += float(
                expense.get("amount", 0)
            )

        if not totals:
            messagebox.showinfo(
                "Category Report",
                "No expenses available yet."
            )
            return

        report = "\n".join(
            f"{category}: ₹{amount:,.2f}"
            for category, amount in sorted(
                totals.items(), key=lambda item: item[1], reverse=True
            )
        )

        messagebox.showinfo("Category Report", report)

    # ---------------- CHART WINDOW ----------------

    def show_charts(self):
        if not self.expenses:
            messagebox.showinfo(
                "No Data",
                "Add some expenses first to view graphical charts."
            )
            return

        chart_window = tk.Toplevel(self.root)
        chart_window.title("Expense Analytics")
        chart_window.geometry("1000x700")
        chart_window.minsize(850, 600)
        chart_window.configure(bg=BG)

        header = tk.Frame(chart_window, bg=BG)
        header.pack(fill="x", padx=25, pady=20)

        tk.Label(
            header,
            text="Expense Analytics",
            bg=BG,
            fg=TEXT,
            font=("Segoe UI", 23, "bold")
        ).pack(side="left")

        tk.Label(
            header,
            text="Visualize your spending habits",
            bg=BG,
            fg=MUTED,
            font=("Segoe UI", 10)
        ).pack(side="right", pady=10)

        # Two chart panels
        charts_frame = tk.Frame(chart_window, bg=BG)
        charts_frame.pack(
            fill="both", expand=True, padx=20, pady=(0, 20)
        )

        category_panel = tk.Frame(
            charts_frame, bg=WHITE, padx=15, pady=15
        )
        category_panel.pack(
            side="left", fill="both", expand=True, padx=(0, 10)
        )

        monthly_panel = tk.Frame(
            charts_frame, bg=WHITE, padx=15, pady=15
        )
        monthly_panel.pack(
            side="left", fill="both", expand=True, padx=(10, 0)
        )

        tk.Label(
            category_panel,
            text="Category-wise Expenses",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 10))

        tk.Label(
            monthly_panel,
            text="Monthly Spending Trend",
            bg=WHITE,
            fg=TEXT,
            font=("Segoe UI", 13, "bold")
        ).pack(anchor="w", pady=(0, 10))

        category_canvas = tk.Canvas(
            category_panel,
            bg=WHITE,
            highlightthickness=0
        )
        category_canvas.pack(fill="both", expand=True)

        monthly_canvas = tk.Canvas(
            monthly_panel,
            bg=WHITE,
            highlightthickness=0
        )
        monthly_canvas.pack(fill="both", expand=True)

        # Draw after the window gets its actual size
        chart_window.update_idletasks()

        self.draw_category_chart(category_canvas)
        self.draw_monthly_chart(monthly_canvas)

    # ---------------- CATEGORY BAR CHART ----------------

    def draw_category_chart(self, canvas):
        canvas.delete("all")

        totals = defaultdict(float)

        for expense in self.expenses:
            category = expense.get("category", "Other")
            totals[category] += float(expense.get("amount", 0))

        if not totals:
            canvas.create_text(
                180, 150, text="No expense data",
                fill=MUTED, font=("Segoe UI", 12)
            )
            return

        width = max(canvas.winfo_width(), 350)
        height = max(canvas.winfo_height(), 350)

        sorted_data = sorted(
            totals.items(), key=lambda item: item[1], reverse=True
        )

        max_value = max(value for _, value in sorted_data)
        colors = [
            "#7565D9", "#21A179", "#F1A34B",
            "#E45B68", "#4A90D9", "#A66DD4",
            "#38A6A6", "#E38BB3"
        ]

        left = 100
        right = width - 25
        bar_height = 24
        gap = 22
        top = 35

        for i, (category, amount) in enumerate(sorted_data):
            y = top + i * (bar_height + gap)

            if y + bar_height > height - 30:
                break

            bar_width = (amount / max_value) * max(20, right - left - 75)

            canvas.create_text(
                left - 10,
                y + bar_height / 2,
                text=category,
                anchor="e",
                fill=TEXT,
                font=("Segoe UI", 9, "bold")
            )

            canvas.create_rectangle(
                left, y, right - 55, y + bar_height,
                fill="#F0EFF7", outline=""
            )

            canvas.create_rectangle(
                left, y, left + bar_width, y + bar_height,
                fill=colors[i % len(colors)], outline=""
            )

            canvas.create_text(
                min(left + bar_width + 8, right),
                y + bar_height / 2,
                text=f"₹{amount:,.0f}",
                anchor="w",
                fill=TEXT,
                font=("Segoe UI", 8, "bold")
            )

        canvas.create_text(
            left, height - 12,
            text="Spending by category",
            anchor="w",
            fill=MUTED,
            font=("Segoe UI", 8)
        )

    # ---------------- MONTHLY BAR CHART ----------------

    def draw_monthly_chart(self, canvas):
        canvas.delete("all")

        monthly_totals = defaultdict(float)

        for expense in self.expenses:
            try:
                date = datetime.strptime(
                    str(expense.get("date", ""))[:10], "%Y-%m-%d"
                )
                month_key = date.strftime("%Y-%m")
                monthly_totals[month_key] += float(
                    expense.get("amount", 0)
                )
            except (ValueError, TypeError):
                continue

        if not monthly_totals:
            canvas.create_text(
                180, 150, text="No valid date data",
                fill=MUTED, font=("Segoe UI", 12)
            )
            return

        now = datetime.today()
        months = []

        for offset in range(5, -1, -1):
            month_number = now.month - offset
            year = now.year

            while month_number <= 0:
                month_number += 12
                year -= 1

            month_date = datetime(year, month_number, 1)
            key = month_date.strftime("%Y-%m")
            label = month_date.strftime("%b")
            months.append((key, label, monthly_totals.get(key, 0)))

        width = max(canvas.winfo_width(), 350)
        height = max(canvas.winfo_height(), 350)

        max_value = max((item[2] for item in months), default=0)
        if max_value <= 0:
            max_value = 1

        left = 45
        right = width - 20
        top = 40
        bottom = height - 65

        canvas.create_line(
            left, top, left, bottom,
            fill="#DADCE7", width=2
        )
        canvas.create_line(
            left, bottom, right, bottom,
            fill="#DADCE7", width=2
        )

        chart_width = right - left
        bar_space = chart_width / 6
        bar_width = min(34, bar_space * 0.55)

        for i, (key, label, amount) in enumerate(months):
            center_x = left + bar_space * (i + 0.5)
            bar_height = (amount / max_value) * (bottom - top - 35)
            bar_top = bottom - bar_height

            if amount > 0:
                canvas.create_rectangle(
                    center_x - bar_width / 2,
                    bar_top,
                    center_x + bar_width / 2,
                    bottom,
                    fill=PURPLE,
                    outline=""
                )

                canvas.create_text(
                    center_x,
                    max(top, bar_top - 12),
                    text=f"{amount:,.0f}",
                    fill=TEXT,
                    font=("Segoe UI", 8, "bold")
                )

            canvas.create_text(
                center_x,
                bottom + 20,
                text=label,
                fill=MUTED,
                font=("Segoe UI", 9, "bold")
            )

        canvas.create_text(
            left, height - 12,
            text="Monthly expenses (₹)",
            anchor="w",
            fill=MUTED,
            font=("Segoe UI", 8)
        )


# ---------------- RUN APPLICATION ----------------

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
