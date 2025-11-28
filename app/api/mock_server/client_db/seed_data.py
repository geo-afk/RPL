from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession
from .models import Transaction, Budget, Employee

# -------------------
# MOCK DATA
# -------------------
mock_transactions = [
    {"date": "2025-11-01", "description": "Server Hosting", "category": "IT", "amount": 1200.50, "status": "completed"},
    {"date": "2025-11-03", "description": "Office Rent", "category": "Facilities", "amount": 5000.00, "status": "pending"},
    {"date": "2025-11-05", "description": "Client Payment", "category": "Revenue", "amount": 15000.00, "status": "completed"},
]

mock_budgets = [
    {"month": "November 2025", "category": "Marketing", "allocated": 8000, "spent": 3000},
    {"month": "November 2025", "category": "IT", "allocated": 5000, "spent": 2200},
    {"month": "November 2025", "category": "HR", "allocated": 10000, "spent": 6500},
]

mock_employees = [
    {"name": "Alice Johnson", "email": "alice@company.com", "department": "Engineering", "salary": 120000, "hire_date": "2023-01-15"},
    {"name": "Bob Smith", "email": "bob@company.com", "department": "Sales", "salary": 95000, "hire_date": "2024-06-20"},
    {"name": "Carol Lee", "email": "carol@company.com", "department": "HR", "salary": 85000, "hire_date": "2022-11-10"},
]

# -------------------
# ASYNC SEED FUNCTION
# -------------------
async def seed(db: AsyncSession) -> bool:
    # Check if already seeded
    existing_txn = await db.exec(select(Transaction))
    if existing_txn.first():
        return False  # Already seeded

    # Add Transactions
    for t in mock_transactions:
        db.add(Transaction(**t))

    # Add Budgets
    for b in mock_budgets:
        db.add(Budget(**b))

    # Add Employees
    for e in mock_employees:
        db.add(Employee(**e))

    # Commit all changes
    await db.commit()
    return True
