from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors


def money(val):
    return f"${val:,.2f}"


def build_tax_report_pdf(buffer, data):
    c = canvas.Canvas(buffer, pagesize=letter)
    width, height = letter

    # 🖼️ Logo
    c.drawImage("app/static/logo.png", 50, height - 80, width=80, height=80)

    # 🧾 Title
    c.setFont("Helvetica-Bold", 20)
    c.drawString(150, height - 50, f"Tax Report {data['year']}")

    # Meta info
    c.setFont("Helvetica", 10)
    c.drawString(150, height - 70, f"First Name: {data['first_name']}")
    c.drawString(150, height - 70, f"Last Name: {data['last_name']}")
    c.drawString(150, height - 85, f"Filing Status: {data['filing_status']}")
    c.drawString(150, height - 100, f"Generated: {data['generated_at']}")

    # Divider
    c.setStrokeColor(colors.grey)
    c.line(50, height - 110, width - 50, height - 110)

    y = height - 140

    def section(title):
        nonlocal y
        c.setFont("Helvetica-Bold", 14)
        c.drawString(50, y, title)
        y -= 20

    def row(label, value):
        nonlocal y
        c.setFont("Helvetica", 12)
        c.drawString(70, y, label)
        c.drawRightString(width - 50, y, value)
        y -= 18

    # 💰 Income
    section("Income")
    row("Total Income", money(data["total_income"]))

    # 💸 Expenses
    section("Expenses")
    row("Total Expenses", money(data["total_expenses"]))

    # 🚗 Mileage
    section("Mileage")
    row("Total Miles", f"{data['total_miles']:,}")
    row("Rate", f"${data['mileage_rate']}")
    row("Deduction", money(data["mileage_deduction"]))

    # 🧾 Deductions
    section("Deductions")
    row("Total Deductions", money(data["total_deductions"]))

    # 📊 Summary
    section("Summary")
    row("Net Profit", money(data["net_profit"]))

    c.setFont("Helvetica-Bold", 12)
    row("Taxable Income", money(data["taxable_income"]))
    row("Estimated Tax Owed", money(data["tax_owed"]))

    # Footer
    c.setFont("Helvetica-Oblique", 9)
    c.setFillColor(colors.grey)
    c.drawString(
        50,
        40,
        "This report is an estimate and should be reviewed by a tax professional."
    )

    c.save()
