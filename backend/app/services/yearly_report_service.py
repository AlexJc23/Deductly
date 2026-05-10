from app.models.milage_rate import MileageRate
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import func
from fastapi import HTTPException
from decimal import Decimal, InvalidOperation
from datetime import datetime, timezone

from app.models import TaxBracket, User, Expense, Income, Trip


def generate_tax_report(db: Session, user: User, year: int):
    try:
        mileage_rate = db.query(func.max(MileageRate.rate)).filter(MileageRate.year == year).scalar() or Decimal("0")

        # 💰 totals
        total_income = (
            db.query(func.sum(Income.amount))
            .filter(
                Income.user_id == user.id,
                func.extract("year", Income.received_at) == year
            )
            .scalar() or Decimal("0")
        )

        total_expenses = (
            db.query(func.sum(Expense.amount))
            .filter(
                Expense.user_id == user.id,
                func.extract("year", Expense.incurred_at) == year
            )
            .scalar() or Decimal("0")
        )

        total_miles = (
            db.query(func.sum(Trip.distance_miles))
            .filter(
                Trip.user_id == user.id,
                func.extract("year", Trip.created_at) == year
            )
            .scalar() or Decimal("0")
        )

        total_income = Decimal(total_income)
        total_expenses = Decimal(total_expenses)
        total_miles = Decimal(total_miles)

        # 🚗 mileage
        mileage_deduction = total_miles * mileage_rate

        # 🧾 deductions
        total_deductions = total_expenses + mileage_deduction

        # 📉 profit
        net_profit = total_income - total_expenses
        taxable_income = max(net_profit - mileage_deduction, Decimal("0"))

        # 🧮 tax calculation
        tax_brackets = (
            db.query(TaxBracket)
            .filter(
                TaxBracket.year == year,
                TaxBracket.filing_status == user.filing_status
            )
            .order_by(TaxBracket.min_income.asc())
            .all()
        )


        if not tax_brackets:
            raise HTTPException(status_code=404, detail="No tax brackets found")

        tax_owed = Decimal("0")
        remaining_income = taxable_income

        for bracket in tax_brackets:
            if remaining_income <= 0:
                break

            lower = bracket.min_income
            upper = bracket.max_income or Decimal("Infinity")
            span = upper - lower

            taxable_in_bracket = min(remaining_income, span)

            tax_owed += taxable_in_bracket * bracket.rate
            remaining_income -= taxable_in_bracket

        return {
            "year": year,
            "first_name": getattr(user, "first_name", "N/A"),
            "last_name": getattr(user, "last_name", "N/A"),
            "filing_status": user.filing_status,
            "generated_at": datetime.now(timezone.utc),

            "total_income": total_income,
            "total_expenses": total_expenses,

            "total_miles": total_miles,
            "mileage_rate": mileage_rate,
            "mileage_deduction": mileage_deduction,

            "total_deductions": total_deductions,
            "net_profit": net_profit,
            "taxable_income": taxable_income,
            "tax_owed": tax_owed,
        }

    except SQLAlchemyError:
        raise HTTPException(status_code=500, detail="Database error while generating report")

    except InvalidOperation:
        raise HTTPException(status_code=500, detail="Decimal calculation error")
