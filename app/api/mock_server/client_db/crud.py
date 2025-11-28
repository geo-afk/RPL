from sqlmodel import Session, select
from .models import Transaction, Budget, Employee

# Map schema+table names to SQLModel classes
TABLE_MODELS = {
    ("DB_Finance", "transactions"): Transaction,
    ("DB_Finance", "budgets"): Budget,
    ("DB_HR", "employees"): Employee,
}


def get_table_model(db_key: str, table_name: str):
    """Return the SQLModel class for a given schema+table."""
    return TABLE_MODELS.get((db_key, table_name))


async def get_rows(db: Session, db_key: str, table_name: str, skip: int = 0, limit: int = 100):
    """Retrieve rows from a table with optional pagination."""
    model = get_table_model(db_key, table_name)
    if not model:
        raise ValueError("Table not found")

    statement = select(model).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results


async def update_row(db: Session, db_key: str, table_name: str, row_id: int, updates: dict):
    """Update a row by ID with a dictionary of changes."""
    model = get_table_model(db_key, table_name)
    if not model:
        raise ValueError("Table not found")

    statement = select(model).where(model.id == row_id)
    row = db.exec(statement).first()
    if not row:
        raise ValueError("Row not found")

    for key, value in updates.items():
        if hasattr(row, key):
            setattr(row, key, value)

    db.add(row)  # Ensure the row is added to the session
    db.commit()
    db.refresh(row)
    return row


async def delete_row(db: Session, db_key: str, table_name: str, row_id: int):
    """Delete a row by ID."""
    model = get_table_model(db_key, table_name)
    if not model:
        raise ValueError("Table not found")

    statement = select(model).where(model.id == row_id)
    row = db.exec(statement).first()
    if row:
        db.delete(row)
        db.commit()
    return row
