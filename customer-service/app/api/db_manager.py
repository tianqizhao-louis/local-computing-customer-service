from app.api.models import CustomerIn, CustomerOut
from app.api.db import customers, database


async def add_customer(payload: CustomerIn):
    query = customers.insert().values(**payload.dict())

    return await database.execute(query=query)

async def get_all_customers():
    query = customers.select()
    return await database.fetch_all(query=query)

# async def get_movie(id):
#     query = movies.select(movies.c.id==id)
#     return await database.fetch_one(query=query)

# async def delete_movie(id: int):
#     query = movies.delete().where(movies.c.id==id)
#     return await database.execute(query=query)

# async def update_movie(id: int, payload: MovieIn):
#     query = (
#         movies
#         .update()
#         .where(movies.c.id == id)
#         .values(**payload.dict())
#     )
#     return await database.execute(query=query)