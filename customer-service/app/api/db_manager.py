from app.api.models import CustomerIn, CustomerOut
from app.api.db import customers, database
from typing import Optional


async def add_customer(payload: CustomerIn, customer_id):
    query = customers.insert().values(id=customer_id, **payload.model_dump())

    return await database.execute(query=query)


async def get_all_customers():
    query = customers.select()
    return await database.fetch_all(query=query)


async def get_customer(id):
    query = customers.select().where(customers.c.id == id)
    return await database.fetch_one(query=query)


async def update_customer(id: str, payload: CustomerIn):
    query = (
        customers.update().where(customers.c.id == id).values(**payload.model_dump())
    )
    return await database.execute(query=query)


async def delete_customer(id: str):
    query = customers.delete().where(customers.c.id == id)
    return await database.execute(query=query)


async def delete_all_customers():
    query = customers.delete()
    return await database.execute(query=query)


# Non-CRUD operations


async def get_customer_by_email(email: str):
    query = customers.select().where(customers.c.email == email)
    return await database.fetch_one(query=query)
