from fastapi import APIRouter, HTTPException, Depends
from database import schemas, models, session
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_pagination import Page
from typing import Optional
from fastapi_pagination import paginate

from api.login_handler import get_current_user_from_token
from api.action import operator

oper_router = APIRouter()


@oper_router.post('', response_model=schemas.ShowOperator)
async def create_new_operator(body:schemas.CreateOperator, db:AsyncSession = Depends(session.get_db),
                              current_user:models.Employees=Depends(get_current_user_from_token)):
    try:
        return await operator._create_new_operatoe(session=db, body=body)
    except ValidationError as e:
        raise HTTPException(
            status_code=422,
            detail=f'Error occured:{e.errors()}'
        )
    
@oper_router.get('', response_model=Page[schemas.ShowOperator])
async def get_all_operators(oper_type_id:Optional[int]=None, status:Optional[str]=None, db:AsyncSession = Depends(session.get_db), search: Optional[str]=None,
                            current_user:models.Employees=Depends(get_current_user_from_token)):
    operator_list = await operator._get_all_operators(operator_type_id=oper_type_id, session=db, status=status, search=search)
    return paginate(operator_list)

@oper_router.post('/status')
async def change_operator_status(oper_id:int, status:str, db:AsyncSession = Depends(session.get_db),
                                 current_user:models.Employees=Depends(get_current_user_from_token)):
    return await operator._change_operator_status(oper_id=oper_id,status=status, session=db)

@oper_router.patch('')
async def update_operator(oper_id:int, update_params:schemas.UpdateOperator, db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    body = update_params.model_dump(exclude_none=True)
    return await operator._update_operator(oper_id=oper_id,
                                           body=body, session=db)

@oper_router.delete('')
async def delete_operator(oper_id:int, db:AsyncSession=Depends(session.get_db),
                          current_user:models.Employees=Depends(get_current_user_from_token)):
    return await operator._delete_oper_by_id(oper_id=oper_id, session=db)
