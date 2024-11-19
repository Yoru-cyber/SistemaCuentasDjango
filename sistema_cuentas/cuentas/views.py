from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.db.models import Sum
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.core.paginator import Paginator
from cuentas.models import Income, Expense
from .forms import IncomeForm, ExpenseForm, ReportForm


# Create your views here.
def index(request):
    context = {}
    return render(request, "cuentas/index.html", context)


def incomes(request):
    incomes = Income.objects.order_by("id")
    paginator = Paginator(incomes, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    form = IncomeForm()
    context = {"page_obj": page_obj, "form": form}
    return render(request, "cuentas/incomes.html", context)


# Detail View
def income_detail(request, pk):
    income = get_object_or_404(Income, pk=pk)
    return render(request, "cuentas/income_detail.html", {"income": income})


# Create View
def income_create(request):
    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("cuentas:incomes"))
    else:
        form = IncomeForm()
    return render(request, "cuentas/income_form.html", {"form": form})


# Update View
def income_update(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        form = IncomeForm(request.POST, instance=income)
        if form.is_valid():
            form.save()
            return redirect(reverse("cuentas:incomes"))
    else:
        form = IncomeForm(instance=income)
    return render(request, "cuentas/income_form.html", {"form": form})


# Delete View
def income_delete(request, pk):
    income = get_object_or_404(Income, pk=pk)
    if request.method == "POST":
        income.delete()
        return redirect(reverse("cuentas:incomes"))
    return render(request, "cuentas/income_confirm_delete.html", {"income": income})


def expenses(request):
    expenses = Expense.objects.order_by("id")
    paginator = Paginator(expenses, 12)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    form = ExpenseForm()
    context = {"page_obj": page_obj, "form": form}
    return render(request, "cuentas/expenses.html", context)


# Create View
def expense_create(request):
    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect(reverse("cuentas:expenses"))
    else:
        form = ExpenseForm()
    return render(request, "cuentas/expense_form.html", {"form": form})


# Update View
def expense_update(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        form = ExpenseForm(request.POST, instance=expense)
        if form.is_valid():
            form.save()
            return redirect(reverse("cuentas:expenses"))
    else:
        form = ExpenseForm(instance=expense)
    return render(request, "cuentas/expense_form.html", {"form": form})


# Delete View
def expense_delete(request, pk):
    expense = get_object_or_404(Expense, pk=pk)
    if request.method == "POST":
        expense.delete()
        return redirect(reverse("cuentas:expenses"))
    return render(request, "cuentas/expense_confirm_delete.html", {"expense": expense})


def reports(request):
    """
    Handles the form to generate a PDF report.
    """
    if request.method == "POST":
        form = ReportForm(request.POST)
        if form.is_valid():
            year = form.cleaned_data["year"]
            month = form.cleaned_data["month"]
            # Redirect to the PDF generation view with query parameters
            return HttpResponseRedirect(
                f"{reverse('cuentas:totals_by_month_year')}?year={year}&month={month}"
            )
    else:
        form = ReportForm()

    return render(request, "cuentas/report_form.html", {"form": form})


def totals_by_month_year(request):
    """
    Filters Incomes and Expenses by month and year from query parameters and returns their totals as a PDF with details.
    """
    try:
        # Extract month and year from query parameters
        year = int(request.GET.get("year", 0))
        month = int(request.GET.get("month", 0))

        # Validate the year and month
        if year < 1 or month < 1 or month > 12:
            raise ValueError("Invalid year or month")

        # Validate using datetime to ensure the date is logical
        datetime(year, month, 1)

        # Filter Incomes and Expenses
        incomes = Income.objects.filter(date__year=year, date__month=month)
        expenses = Expense.objects.filter(date__year=year, date__month=month)
        incomes_total = incomes.aggregate(total=Sum("value"))["total"] or 0
        expenses_total = expenses.aggregate(total=Sum("value"))["total"] or 0

        # Create the PDF response
        response = HttpResponse(content_type="application/pdf")
        response["Content-Disposition"] = (
            f'attachment; filename="totales_{year}_{month}.pdf"'
        )

        # Create the document
        doc = SimpleDocTemplate(response, pagesize=letter)
        elements = []

        # Title
        styles = getSampleStyleSheet()
        title = Paragraph(f"Reporte de Totales {year}-{month:02d}", styles["Title"])
        elements.append(title)

        # Totals
        totals_data = [
            ["Total Entradas", f"{incomes_total:.2f}"],
            ["Total Salidas", f"{expenses_total:.2f}"],
        ]
        totals_table = Table(totals_data, colWidths=[200, 200])
        totals_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(totals_table)
        elements.append(Paragraph("\n", styles["BodyText"]))

        # Detailed Table
        details_data = [["Tipo", "Nombre", "Categoría", "Valor", "Fecha"]]
        for income in incomes:
            details_data.append(
                [
                    "Entradas",
                    income.name,
                    income.category,
                    f"{income.value:.2f}",
                    income.date.strftime("%Y-%m-%d"),
                ]
            )
        for expense in expenses:
            details_data.append(
                [
                    "Salidas",
                    expense.name,
                    expense.category,
                    f"{expense.value:.2f}",
                    expense.date.strftime("%Y-%m-%d"),
                ]
            )

        details_table = Table(details_data, colWidths=[80, 120, 120, 80, 80])
        details_table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                    ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                    ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                ]
            )
        )
        elements.append(details_table)

        # Build the PDF
        doc.build(elements)
        return response

    except ValueError:
        return HttpResponse(
            "Invalid year or month", status=400, content_type="text/plain"
        )
