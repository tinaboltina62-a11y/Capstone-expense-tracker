import flet as ft
import json
import os
from datetime import datetime

DATA_FILE = "data/expenses.json"

class Expense:
    def __init__(self, title, amount, category):
        self.title = title
        self.amount = float(amount)
        self.category = category
        self.date = datetime.now().strftime("%Y-%m-%d")
    def to_dict(self):
        return self.__dict__

def load_expenses():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_expense(exp):
    data = load_expenses()
    data.append(exp.to_dict())
    os.makedirs("data", exist_ok=True)
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=2)

def main(page: ft.Page):
    page.title = "My Expense Tracker"
    page.theme = ft.Theme(color_scheme_seed="blue")
    page.padding = 20
    def route_change(e):
        page.views.clear()
        home_list = ft.Column()
        for ex in load_expenses():
            home_list.controls.append(ft.ListTile(title=ft.Text(f"{ex['title']} - R{ex['amount']}"), subtitle=ft.Text(ex['category'])))
        home = ft.View("/", [ft.AppBar(title=ft.Text("Home")), ft.Text("My Expenses", size=24, weight="bold"), home_list, ft.ElevatedButton("Add Expense", on_click=lambda _: page.go("/add"))])
        title_input = ft.TextField(label="Title")
        amount_input = ft.TextField(label="Amount")
        category_input = ft.Dropdown(label="Category", options=[ft.dropdown.Option("Food"), ft.dropdown.Option("Transport"), ft.dropdown.Option("Study")])
        def save_click(e):
            if title_input.value and amount_input.value:
                save_expense(Expense(title_input.value, amount_input.value, category_input.value or "General"))
                page.go("/")
        add_view = ft.View("/add", [ft.AppBar(title=ft.Text("Add Expense")), title_input, amount_input, category_input, ft.ElevatedButton("Save", on_click=save_click), ft.TextButton("Back", on_click=lambda _: page.go("/"))])
        page.views.append(home)
        if page.route == "/add":
            page.views.append(add_view)
        page.update()
    page.on_route_change = route_change
    page.go("/")
ft.app(main)
