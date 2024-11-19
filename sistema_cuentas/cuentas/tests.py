from django.test import TestCase
from datetime import date
from decimal import Decimal

from django.urls import reverse
from .models import Expense, Income


# Create your tests here.
class ExpenseModelTest(TestCase):
    def setUp(self):
        self.expense_data = {
            "name": "Groceries",
            "category": "Food",
            "value": Decimal("150.75"),
            "date": date(2024, 11, 19),
        }
        self.expense = Expense.objects.create(**self.expense_data)

    def test_create_expense(self):
        self.assertEqual(self.expense.name, "Groceries")
        self.assertEqual(self.expense.category, "Food")
        self.assertEqual(self.expense.value, Decimal("150.75"))
        self.assertEqual(self.expense.date, date(2024, 11, 19))
        self.assertIsNotNone(self.expense.created_at)
        self.assertIsNotNone(self.expense.updated_at)

    def test_update_expense(self):
        self.expense.name = "Supermarket"
        self.expense.value = Decimal("200.50")
        self.expense.save()

        updated_expense = Expense.objects.get(id=self.expense.id)
        self.assertEqual(updated_expense.name, "Supermarket")
        self.assertEqual(updated_expense.value, Decimal("200.50"))

    # def test_string_representation(self):
    #     self.assertEqual(str(self.expense), "Groceries")  # Modify if __str__ is added.


class IncomeModelTest(TestCase):
    def setUp(self):
        self.income_data = {
            "name": "Salary",
            "category": "Work",
            "value": Decimal("3000.00"),
            "date": date(2024, 11, 19),
        }
        self.income = Income.objects.create(**self.income_data)

    def test_create_income(self):
        self.assertEqual(self.income.name, "Salary")
        self.assertEqual(self.income.category, "Work")
        self.assertEqual(self.income.value, Decimal("3000.00"))
        self.assertEqual(self.income.date, date(2024, 11, 19))
        self.assertIsNotNone(self.income.created_at)
        self.assertIsNotNone(self.income.updated_at)

    def test_update_income(self):
        self.income.category = "Freelance"
        self.income.value = Decimal("4500.00")
        self.income.save()

        updated_income = Income.objects.get(id=self.income.id)
        self.assertEqual(updated_income.category, "Freelance")
        self.assertEqual(updated_income.value, Decimal("4500.00"))

    # def test_string_representation(self):
    #     self.assertEqual(str(self.income), "Salary")  # Modify if __str__ is added.


from django.test import TestCase
from django.urls import reverse
from datetime import date
from decimal import Decimal
from .models import Income, Expense


class IncomeViewTest(TestCase):
    def setUp(self):
        self.income = Income.objects.create(
            name="Salary",
            category="Work",
            value=Decimal("3000.00"),
            date=date(2024, 11, 19),
        )

    def test_incomes_list(self):
        response = self.client.get(reverse("cuentas:incomes"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Salary")

    # def test_income_detail(self):
    #     response = self.client.get(reverse("cuentas:income_detail", args=[self.income.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Salary")

    def test_income_create(self):
        data = {
            "name": "Freelance",
            "category": "Work",
            "value": "1500.00",
            "date": "2024-11-20",
        }
        response = self.client.post(reverse("cuentas:income_create"), data)
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Income.objects.filter(name="Freelance").exists())

    def test_income_update(self):
        data = {
            "name": "Updated Salary",
            "category": "Work",
            "value": "3500.00",
            "date": "2024-11-19",
        }
        response = self.client.post(
            reverse("cuentas:income_update", args=[self.income.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.income.refresh_from_db()
        self.assertEqual(self.income.name, "Updated Salary")
        self.assertEqual(self.income.value, Decimal("3500.00"))

    def test_income_delete(self):
        response = self.client.post(
            reverse("cuentas:income_delete", args=[self.income.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Income.objects.filter(pk=self.income.pk).exists())


class ExpenseViewTest(TestCase):
    def setUp(self):
        self.expense = Expense.objects.create(
            name="Groceries",
            category="Food",
            value=Decimal("150.75"),
            date=date(2024, 11, 19),
        )

    def test_expenses_list(self):
        response = self.client.get(reverse("cuentas:expenses"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Groceries")

    # def test_expense_detail(self):
    #     response = self.client.get(reverse("cuentas:expense_detail", args=[self.expense.pk]))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertContains(response, "Groceries")

    def test_expense_create(self):
        data = {
            "name": "Shopping",
            "category": "Clothing",
            "value": "250.00",
            "date": "2024-11-20",
        }
        response = self.client.post(reverse("cuentas:expense_create"), data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Expense.objects.filter(name="Shopping").exists())

    def test_expense_update(self):
        data = {
            "name": "Updated Groceries",
            "category": "Food",
            "value": "200.00",
            "date": "2024-11-19",
        }
        response = self.client.post(
            reverse("cuentas:expense_update", args=[self.expense.pk]), data
        )
        self.assertEqual(response.status_code, 302)
        self.expense.refresh_from_db()
        self.assertEqual(self.expense.name, "Updated Groceries")
        self.assertEqual(self.expense.value, Decimal("200.00"))

    def test_expense_delete(self):
        response = self.client.post(
            reverse("cuentas:expense_delete", args=[self.expense.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Expense.objects.filter(pk=self.expense.pk).exists())
