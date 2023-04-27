"""FAST API DEMOS"""
from datetime import datetime
import pyodbc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, validator


app = FastAPI()
CONNECTION_STRING = "Driver={ODBC Driver 17 for SQL Server};\
                    Server=localhost,1433;UID=sa;PWD=Password123;"
DB_NAME = "Vegards_sales"
cnxn = pyodbc.connect(CONNECTION_STRING, autocommit=True)


class Sale(BaseModel):
    """Class for a sale"""

    sales_date: str
    buyer: str
    apples: str
    oranges: str

    @validator("sales_date")
    def date_is_datetime(cls, value):
        """Verify that date is datetime"""
        try:
            sales_date = datetime.strptime(value, "%Y-%m-%d").date()
            return sales_date
        except ValueError as value_error:
            raise HTTPException(
                status_code=400,
                detail="Invalid sales date format. Use the YYYY-MM-DD format.",
            ) from value_error

    @validator("buyer")
    def name_is_letters_and_spaces(cls, value):
        """Verify that name is letters and spaces"""
        if not all(x.isalpha() or x.isspace() for x in value):
            raise HTTPException(
                status_code=400,
                detail="Invalid sales person name. Name cannot contain numbers.",
            )
        return value

    @validator("apples")
    def apples_is_int(cls, value):
        """Verify that number of apples is int"""
        try:
            return int(value)
        except ValueError as value_error:
            raise HTTPException(
                status_code=400,
                detail="Apples must be an integer",
            ) from value_error

    @validator("oranges")
    def oranges_is_int(cls, value):
        """Verify that number of oranges is int"""
        try:
            return int(value)
        except ValueError as value_error:
            raise HTTPException(
                status_code=400,
                detail="Oranges must be an integer",
            ) from value_error


@app.post("/api/sales")
async def create_sale(sale: Sale):
    """Function to insert the data into the sales table"""
    cursor = cnxn.cursor()
    create_db = f"IF NOT EXISTS(SELECT * FROM sys.databases WHERE name = '{DB_NAME}')\
               BEGIN CREATE DATABASE [{DB_NAME}] END"
    cursor.execute(create_db)
    change_db = f"USE {DB_NAME}"
    cursor.execute(change_db)

    create_table = (
        "IF NOT EXISTS(SELECT name FROM sys.tables WHERE name = 'Inventory') BEGIN;"
    )
    table_data = "CREATE TABLE Inventory (sales_id INT NOT NULL IDENTITY PRIMARY KEY, \
                  sales_date VARCHAR(10), buyer VARCHAR(30),  apples INT, oranges INT);"
    end_table = "END"
    cursor.execute(create_table + table_data + end_table)

    cursor.execute(
        "INSERT INTO Inventory (sales_date, buyer, apples, oranges) \
         VALUES (?, ?, ?, ?)",
        sale.sales_date,
        sale.buyer,
        sale.apples,
        sale.oranges,
    )
    cursor.commit()
    return "Sale created successfully"
