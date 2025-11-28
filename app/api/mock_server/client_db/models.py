from typing import Optional
from sqlmodel import SQLModel, Field


class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"
    __table_args__ = {"schema": "DB_Finance"}

    id: Optional[int] = Field(default=None, primary_key=True)
    date: str
    description: str
    category: str
    amount: float
    status: str = Field(default="completed")


class Budget(SQLModel, table=True):
    __tablename__ = "budgets"
    __table_args__ = {"schema": "DB_Finance"}

    id: Optional[int] = Field(default=None, primary_key=True)
    month: str
    category: str
    allocated: float
    spent: float


class Employee(SQLModel, table=True):
    __tablename__ = "employees"
    __table_args__ = {"schema": "DB_HR"}

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(unique=True)
    department: str
    salary: float
    hire_date: str
