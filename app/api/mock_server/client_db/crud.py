from sqlmodel import Session, select
from typing import Tuple, List
from sqlmodel import select
from .models import Transaction, Budget, Employee

# Map schema+table names to SQLModel classes
TABLE_MODELS = {
    ("DB_Finance", "transactions"): Transaction,
    ("DB_Finance", "budgets"): Budget,
    ("DB_HR", "employees"): Employee,
}

def get_table_details() -> List[Tuple]:
    details = []
    for model in TABLE_MODELS.keys():
        details.append(model)
    return details



def get_table_model(db_key: str, table_name: str):
    """Return the SQLModel class for a given schema+table."""
    return TABLE_MODELS.get((db_key, table_name))


def get_rows(db: Session, db_key: str, table_name: str, skip: int = 0, limit: int = 100):
    """Retrieve rows from a table with optional pagination."""
    model = get_table_model(db_key, table_name)
    if not model:
        raise ValueError("Table not found")

    statement = select(model).offset(skip).limit(limit)
    results = db.exec(statement).all()
    return results



from sqlmodel import select
from typing import Any

def update_row(db: Session, db_key: str, table_name: str, row_id: int, updates: dict) -> Any:
    """Update a row by ID – works with SQLModel + SQLAlchemy 2.0"""
    model = get_table_model(db_key, table_name)
    if not model:
        raise ValueError("Table not found")

    # 1. Fetch the actual model instance
    row = db.get(model, row_id)
    if not row:
        raise ValueError("Row not found")

    # 2. Build a mapping of field_name → Python type from the SQLModel
    # Works with both Pydantic v1 and v2
    fields = getattr(model, "model_fields", None) or model.__fields__
    field_types = {
        name: field_info.annotation or field_info.type_
        for name, field_info in fields.items()
    }

    # 3. Apply updates with proper type conversion
    for key, raw_value in updates.items():
        if key not in field_types:
            continue  # or raise ValueError(f"Field {key} does not exist") for strict mode

        target_type = field_types[key]

        # Handle empty string → NULL
        if raw_value == "" or raw_value is None:
            value = None
        # Convert string numbers coming from JSON
        elif target_type == int and isinstance(raw_value, str):
            try:
                value = int(raw_value)
            except ValueError:
                raise ValueError(f"Cannot convert '{raw_value}' to int for field '{key}'")
        elif target_type == float and isinstance(raw_value, str):
            value = float(raw_value)
        elif target_type == bool:
            value = str(raw_value).lower() in ("true", "1", "yes", "on", "t")
        else:
            value = raw_value

        setattr(row, key, value)

    # 4. Commit – no need for db.add() because db.get() returns a tracked instance
    db.commit()
    db.refresh(row)
    return row


def delete_row(db: Session, db_key: str, table_name: str, row_id: int):
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
