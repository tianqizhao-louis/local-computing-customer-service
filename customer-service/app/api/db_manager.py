import uuid
from databases import Database
from sqlalchemy import select, insert, update, delete
from app.api.db import database, customers, waitlist

# Customer Management

# Add a new customer
async def add_customer(payload, customer_id):
    query = customers.insert().values(
        id=customer_id,
        name=payload.name,
        email=payload.email
    )
    await database.execute(query)

# Get all customers
async def get_all_customers():
    query = customers.select()
    return await database.fetch_all(query)

# Get a specific customer by ID
async def get_customer(customer_id):
    query = customers.select().where(customers.c.id == customer_id)
    return await database.fetch_one(query)

# Get a customer by email
async def get_customer_by_email(email):
    query = customers.select().where(customers.c.email == email)
    return await database.fetch_one(query)

# Update customer details
async def update_customer(customer_id, payload):
    query = (
        update(customers)
        .where(customers.c.id == customer_id)
        .values(name=payload.name, email=payload.email)
    )
    await database.execute(query)

# Delete a customer
async def delete_customer(customer_id):
    query = delete(customers).where(customers.c.id == customer_id)
    await database.execute(query)

# Delete all customers
async def delete_all_customers():
    query = delete(customers)
    await database.execute(query)

# Waitlist Management

# Add a pet to the waitlist
async def add_to_waitlist(consumer_id: str, pet_id: str, breeder_id: str, waitlist_entry_id: str):
    query = waitlist.insert().values(
        id=waitlist_entry_id,
        consumer_id=consumer_id,
        pet_id=pet_id,
        breeder_id=breeder_id
    )
    await database.execute(query)

# Get all waitlist entries for a customer
async def get_waitlist_for_customer(consumer_id: str):
    query = waitlist.select().where(waitlist.c.consumer_id == consumer_id)
    return await database.fetch_all(query)

# Remove a pet from the waitlist
async def remove_from_waitlist(waitlist_entry_id: str):
    query = delete(waitlist).where(waitlist.c.id == waitlist_entry_id)
    await database.execute(query)

# Get a specific waitlist entry by ID
async def get_waitlist_entry(waitlist_entry_id: str):
    query = waitlist.select().where(waitlist.c.id == waitlist_entry_id)
    return await database.fetch_one(query)
