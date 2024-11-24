from typing import List
from fastapi import APIRouter, HTTPException, Response
import os
import uuid
from app.api.models import (
    CustomerOut,
    CustomerIn,
    Link,
    CustomerUpdate,
    CustomerListResponse,
    WaitlistEntryIn,
    WaitlistEntryOut,
)
from app.api import db_manager

customers = APIRouter()
URL_PREFIX = os.getenv("URL_PREFIX")

# Create a new customer
@customers.post("/", response_model=CustomerOut, status_code=201)
async def create_customer(payload: CustomerIn, response: Response):
    customer_id = str(uuid.uuid4())
    await db_manager.add_customer(payload, customer_id)

    customer_url = generate_customer_url(customer_id)
    response.headers["Location"] = customer_url
    response.headers["Link"] = (
        f'<{customer_url}>; rel="self", <{URL_PREFIX}/customers/>; rel="collection"'
    )

    response_data = CustomerOut(
        id=customer_id,
        name=payload.name,
        email=payload.email,
        links=[
            Link(rel="self", href=customer_url),
            Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
        ],
    )
    return response_data

# Get all customers
@customers.get("/", response_model=CustomerListResponse)
async def get_customers():
    db_records = await db_manager.get_all_customers()

    customers = [
        CustomerOut(
            id=db_record["id"],
            name=db_record["name"],
            email=db_record["email"],
            links=[
                Link(rel="self", href=generate_customer_url(db_record["id"])),
                Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
            ],
        )
        for db_record in db_records
    ]

    links = [
        Link(rel="self", href=f"{URL_PREFIX}/customers/"),
        Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
    ]

    return CustomerListResponse(
        data=customers,  # List of CustomerOut instances
        links=links,  # List of Link instances
    )

# Get a specific customer by ID
@customers.get("/{id}/", response_model=CustomerOut)
async def get_customer(id: str):
    customer = await db_manager.get_customer(id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    response_data = CustomerOut(
        id=customer["id"],
        name=customer["name"],
        email=customer["email"],
        links=[
            Link(rel="self", href=generate_customer_url(id)),
            Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
        ],
    )
    return response_data

# Update customer details
@customers.put("/{id}/", response_model=CustomerOut)
async def update_customer(id: str, payload: CustomerUpdate):
    customer = await db_manager.get_customer(id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    updated_data = payload.model_dump(exclude_unset=True)
    customer_in_db = CustomerIn(**customer)
    updated_customer = customer_in_db.model_copy(update=updated_data)

    await db_manager.update_customer(id, updated_customer)
    updated_customer_in_db = await db_manager.get_customer(id)

    response_data = CustomerOut(
        id=updated_customer_in_db["id"],
        name=updated_customer_in_db["name"],
        email=updated_customer_in_db["email"],
        links=[
            Link(rel="self", href=generate_customer_url(id)),
            Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
        ],
    )

    return response_data

# Delete a customer
@customers.delete("/{id}/", response_model=None)
async def delete_customer(id: str):
    customer = await db_manager.get_customer(id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db_manager.delete_customer(id)

# Delete all customers
@customers.delete("/delete/all/", response_model=None)
async def delete_all_customers():
    try:
        await db_manager.delete_all_customers()
        return {"message": "All customers have been deleted."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete all customers: {str(e)}"
        )

# Non-CRUD operations

# Get a customer by email
@customers.get("/email/{email}/", response_model=CustomerOut, status_code=200)
async def get_customer_by_email(email: str):
    customer = await db_manager.get_customer_by_email(email)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    response_data = CustomerOut(
        id=customer["id"],
        name=customer["name"],
        email=customer["email"],
        links=[
            Link(rel="self", href=generate_customer_url(customer["id"])),
            Link(rel="collection", href=f"{URL_PREFIX}/customers/"),
        ],
    )
    return response_data

# Waitlist Management

# Add a pet to the waitlist
@customers.post("/{customer_id}/waitlist", response_model=WaitlistEntryOut, status_code=201)
async def add_to_waitlist(customer_id: str, payload: WaitlistEntryIn):
    # Verify the customer exists
    customer = await db_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Add pet to the waitlist
    waitlist_entry_id = str(uuid.uuid4())
    await db_manager.add_to_waitlist(customer_id, payload.pet_id, payload.breeder_id, waitlist_entry_id)

    response_data = WaitlistEntryOut(
        id=waitlist_entry_id,
        consumer_id=customer_id,
        pet_id=payload.pet_id,
        breeder_id=payload.breeder_id,
    )
    return response_data

# Get the customer's waitlist
@customers.get("/{customer_id}/waitlist", response_model=List[WaitlistEntryOut])
async def get_customer_waitlist(customer_id: str):
    # Verify the customer exists
    customer = await db_manager.get_customer(customer_id)
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Retrieve waitlist
    waitlist_entries = await db_manager.get_waitlist_for_customer(customer_id)

    return [WaitlistEntryOut(**entry) for entry in waitlist_entries]

# Helper function to generate customer URL
def generate_customer_url(customer_id: str):
    return f"{URL_PREFIX}/customers/{customer_id}/"

@customers.get("/breeder/{breeder_id}/waitlist", response_model=List[dict])
async def get_waitlist_for_breeder(breeder_id: str):
    # Verify the breeder exists in the waitlist table
    breeder_exists = await db_manager.verify_breeder_exists(breeder_id)
    if not breeder_exists:
        return [{"message": "Breeder not found in the waitlist"}]
    
    # Retrieve all waitlist entries for the specific breeder
    waitlist_entries = await db_manager.get_waitlist_for_breeder(breeder_id)
    
    # Prepare the response data
    customers_data = []
    for entry in waitlist_entries:
        customer = await db_manager.get_customer(entry["consumer_id"])
        if customer:
            customers_data.append({
                "id": customer["id"],
                "name": customer["name"],
                "email": customer["email"],
                "pet_id": entry["pet_id"]
            })
    
    if not customers_data:
        return [{"message": "No waitlist entries found for this breeder"}]

    return customers_data


