from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from rest_fastapi.bases import ListArgsSchema, ListFilterSchema
from rest_fastapi.core import get_database
from rest_fastapi.demo_api.schemas.demo import CreateDemoSchema
from rest_fastapi.demo_api.services import demo_service
from rest_fastapi.libs.pagination import Pagination

router = APIRouter(prefix='/demo', tags=['demo'])


@router.post('', status_code=201, name='create')
async def create(body: CreateDemoSchema, db: Session = Depends(get_database)):
    user = await demo_service.create(db, body)
    return user.to_dict()


@router.get('', status_code=200, name='list')
async def get_list(name: str = Query(default=None, title='name'),
                   pagination=Depends(Pagination),
                   db: Session = Depends(get_database)):
    args = ListArgsSchema(
        page=pagination.page,
        size=pagination.size
    )
    if name:
        args.filters = [ListFilterSchema(
            key='name',
            condition='like',
            value=name
        )]
    return await demo_service.list(db, args)


@router.get('/{pk}', status_code=200, name='get')
async def get(pk: int, db: Session = Depends(get_database)):
    user = await demo_service.get(db, pk)
    return user.to_dict()


@router.delete('/{pk}', status_code=200, name='delete')
async def delete(pk: int, db: Session = Depends(get_database)):
    await demo_service.delete(db, pk)
    return
