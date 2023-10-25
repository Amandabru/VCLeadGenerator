import sqlite3
from pydantic import BaseModel

from fastapi import FastAPI

db = "dev"

con = sqlite3.connect(db + ".db")
app = FastAPI()


class Company(BaseModel):
    name: str
    industry: str
    size: int
    description: str
    business: str
    founders: str | None = None
    website: str


@app.get("/fetch/{amount}")
async def fetch(amount) -> list[Company]:
    companies = []
    for row in con.cursor().execute("SELECT * FROM company WHERE business_summary IS NOT NULL").fetchmany(int(amount)):
        companies.append(Company(
            name=row[1],
            industry=row[2],
            size=row[3],
            description=row[4],
            business=row[5],
            founders=row[6],
            website=row[7],
        ))
    return companies
