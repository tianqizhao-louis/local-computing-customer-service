from typing import List
from fastapi import APIRouter, HTTPException

from app.api.models import CustomerOut, CustomerIn
from app.api import db_manager
# from app.api.service import is_cast_present

customers = APIRouter()

@customers.post('/', response_model=CustomerOut, status_code=201)
async def create_customer(payload: CustomerIn):
    # for cast_id in payload.casts_id:
    #     if not is_cast_present(cast_id):
    #         raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

    customer_id = await db_manager.add_customer(payload)
    response = {
        'id': customer_id,
        **payload.dict()
    }

    return response

@customers.get('/', response_model=List[CustomerOut])
async def get_customers():
    return await db_manager.get_all_customers()

# @movies.get('/{id}/', response_model=MovieOut)
# async def get_movie(id: int):
#     movie = await db_manager.get_movie(id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return movie

# @movies.put('/{id}/', response_model=MovieOut)
# async def update_movie(id: int, payload: MovieUpdate):
#     movie = await db_manager.get_movie(id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")

#     update_data = payload.dict(exclude_unset=True)

#     if 'casts_id' in update_data:
#         for cast_id in payload.casts_id:
#             if not is_cast_present(cast_id):
#                 raise HTTPException(status_code=404, detail=f"Cast with given id:{cast_id} not found")

#     movie_in_db = MovieIn(**movie)

#     updated_movie = movie_in_db.copy(update=update_data)

#     return await db_manager.update_movie(id, updated_movie)

# @movies.delete('/{id}/', response_model=None)
# async def delete_movie(id: int):
#     movie = await db_manager.get_movie(id)
#     if not movie:
#         raise HTTPException(status_code=404, detail="Movie not found")
#     return await db_manager.delete_movie(id)
