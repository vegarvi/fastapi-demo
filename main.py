"""FAST API DEMO"""
from datetime import datetime
import pyodbc
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


app = FastAPI()

# Replace the server, database, username, and password with your own values
# connection_string = 'Driver={ODBC Driver 17 for SQL Server};Server=localhost
# ,1433;Database=Sales;UID=sa;PWD=Password123;'
connection_string = "Driver={ODBC Driver 17 for SQL Server};\
Server=localhost,1433;UID=sa;PWD=Password123;"

cnxn = pyodbc.connect(connection_string, autocommit=True)


class Sale(BaseModel):
    """Class for a sale"""

    sales_date: str
    buyer: str
    apples: int
    oranges: int


@app.post("/api/sales")
async def create_sale(sale: Sale):

    # Validate the input data
    try:
        sales_date = datetime.strptime(sale.sales_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail="Invalid sales date format. Use the YYYY-MM-DD format.",
        )

    if not sale.buyer.isalpha():
        raise HTTPException(
            status_code=400,
            detail="Invalid sales person name. Name cannot contain numbers.",
        )

    if not sale.apples:
        sale.apples = 0
    if not sale.oranges:
        sale.oranges = 0

    # Insert the data into the shopping_list table
    cursor = cnxn.cursor()

    try:
        cursor.execute("USE Vegards_sales_app")
    except:
        cursor.execute("CREATE DATABASE Vegards_sales_app")
        cursor.execute("USE Vegards_sales_app")
        cursor.execute(
            "CREATE TABLE Inventory (\
             sales_id INT NOT NULL IDENTITY PRIMARY KEY,\
             sales_date VARCHAR(10), buyer VARCHAR(30),\
             apples INT, oranges INT)"
        )
    cursor.execute(
        "INSERT INTO Inventory (sales_date, buyer, apples, oranges) VALUES (?, ?, ?, ?)",
        sales_date,
        sale.buyer,
        sale.apples,
        sale.oranges,
    )
    cursor.commit()
    return "Sale created successfully"
