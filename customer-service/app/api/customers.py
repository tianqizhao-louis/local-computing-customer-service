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
)
from app.api import db_manager

# from app.api.service import is_cast_present

customers = APIRouter()
URL_PREFIX = os.getenv("URL_PREFIX")


@customers.post("/", response_model=CustomerOut, status_code=201)
async def create_customer(payload: CustomerIn, response: Response):
    # for cast_id in payload.casts_id:
    #     if not is_cast_present(cast_id):
    #         raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    customer_id = str(uuid.uuid4())
    await db_manager.add_customer(payload, customer_id)

    customer_url = generate_customer_url(customer_id)
    response.headers["Location"] = customer_url

    response.headers["Link"] = (
        f'<{customer_url}>; rel="self", <URL_PREFIX/customers/>; rel="collection"'
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
        data=customers,  # List of BreederOut instances
        links=links,  # List of Link instances
    )


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


@customers.delete("/{id}/", response_model=None)
async def delete_customer(id: str):
    customer = await db_manager.get_customer(id)

    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found")

    await db_manager.delete_customer(id)


@customers.delete("/delete/all/", response_model=None)
async def delete_all_customers():
    try:
        await db_manager.delete_all_customers()
        return {"message": "All customers have been deleted."}
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Failed to delete all customers: {str(e)}"
        )


def generate_customer_url(customer_id: str):
    return f"{URL_PREFIX}/customers/{customer_id}/"


# Non-CRUD operations


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
