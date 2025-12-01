from fastapi import Depends, HTTPException, Path, APIRouter, status
from sqlalchemy.orm import Session
from typing import List, Dict, Tuple
from app.api.mock_server.client_db.crud import get_rows, delete_row, update_row, get_table_details
from app.api.mock_server.client_db.db_service import get_client_db
from app.api.mock_server.client_db.models import RowUpdatePayload
from app.api.mock_server.client_db.seed_data import seed


def ensure_seeded(db: Session = Depends(get_client_db)):
    seeded = seed(db)
    if seeded:
        print("Database seeded for router!")
    else:
        print("Database already initialized.")


client_db_router = APIRouter(
    prefix="/api",
    tags=["client_db"],
    dependencies=[Depends(ensure_seeded)],
)



@client_db_router.get(
    "/databases/see/tables",
    response_model=List[Tuple],
    status_code=status.HTTP_200_OK,
    summary="Get available tables and their schemas",
    description="Retrieve details of the available tables and which schema they belong.",
)
async def read_rows():
    return get_table_details()



@client_db_router.get(
    "/databases/{db_key}/tables/{table_name}/rows",
    response_model=List[Dict],
    status_code=status.HTTP_200_OK,
    summary="Get rows from a table",
    description="Retrieve rows from a given table in the specified database, supports pagination via query parameters",
)
async def read_rows(
    db_key: str = Path(..., description="Database key, e.g., DB_Finance"),
    table_name: str = Path(..., description="Table name, e.g., transactions"),
    db: Session = Depends(get_client_db),
):
    try:
        rows = get_rows(db, db_key, table_name)
        return [
            {k: v for k, v in row.__dict__.items() if k != "_sa_instance_state"}
            for row in rows
        ]
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))





@client_db_router.patch(
    "/databases/{db_key}/tables/{table_name}/rows/{row_id}",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Update a row",
    description="Update a specific row in the table using a JSON dictionary of changes",
)
async def update_table_row(
        payload: RowUpdatePayload,
        db_key: str = Path(..., description="Database key, e.g., DB_Finance"),
        table_name: str = Path(..., description="Table name, e.g., transactions"),
        row_id: int = Path(..., description="ID of the row to update"),
        db: Session = Depends(get_client_db),
):
    try:
        updated_row = update_row(db, db_key, table_name, row_id, payload.updates)
        data = updated_row.model_dump() if hasattr(updated_row, "model_dump") else updated_row.dict()
        return {"success": True, "updated": data}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))



@client_db_router.delete(
    "/databases/{db_key}/tables/{table_name}/rows/{row_id}",
    response_model=Dict,
    status_code=status.HTTP_200_OK,
    summary="Delete a row",
    description="Delete a specific row in the table by ID",
)
async def delete_table_row(
    db_key: str = Path(..., description="Database key, e.g., DB_Finance"),
    table_name: str = Path(..., description="Table name, e.g., transactions"),
    row_id: int = Path(..., description="ID of the row to delete"),
    db: Session = Depends(get_client_db),
):
    try:
        deleted_row = delete_row(db, db_key, table_name, row_id)
        if not deleted_row:
            raise HTTPException(status_code=404, detail="Row not found")
        return {"success": True, "deleted_id": row_id}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
