from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException

from database import schemas
from dals.operator_dal import OperatorDal


async def _create_new_operatoe(session:AsyncSession, 
                               body:schemas.CreateOperator):
    try:
        async with session.begin():
            emp_dal = OperatorDal(session)
            oper_user = await emp_dal.create_operator(
                full_name=body.full_name,
                phone_number=body.phone_number,
                description=body.description,
                operator_type_id=body.operator_type_id
            )
            operator = await emp_dal.get_operator_type_by_id(oper_user.operator_type_id)

            return schemas.ShowOperator(
                id=oper_user.id,
                full_name=oper_user.full_name,
                phone_number=oper_user.phone_number,
                description=oper_user.description,
                operator_type_id= oper_user.operator_type_id,
                operator_type=operator,
                status=oper_user.status
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_all_operators(session:AsyncSession,
                                operator_type_id:int,
                                status:str, search:str):
    try:
        async with session.begin():
            emp_user = OperatorDal(session)
            operator_all = await emp_user.get_all_operator(oper_type_id=operator_type_id,status=status, search=search)

            return [
                schemas.ShowOperator(
                    id = oper_user.id,
                    full_name= oper_user.full_name,
                    phone_number = oper_user.phone_number,
                    description = oper_user.description,
                    operator_type_id = oper_user.operator_type_id,
                    operator_type = oper_user.operator_type.name,
                    status =  oper_user.status,
                    )
                    for oper_user in operator_all 
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _change_operator_status(session:AsyncSession,
                                  oper_id:int,
                                  status:str):
    try:
        async with session.begin():
            dal_user = OperatorDal(session)
            change_status = await dal_user.change_operator_status(oper_id=oper_id,
                                                                status=status)
            if change_status:
                return {'success':True,
                        'message':'Muvafaqiyatli ozgartirildi'}
            
            return {'success':False,
                        'message':'Muvafaqiyatli ozgartirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_operator(session:AsyncSession, oper_id:int, body:dict):
    try:
        emp_dal = OperatorDal(session)

        update_oper = await emp_dal.update_operator_by_type(oper_id=oper_id, **body)

        return schemas.ShowOperator(
                id = update_oper.id,
                full_name= update_oper.full_name,
                phone_number = update_oper.phone_number,
                description = update_oper.description,
                operator_type_id = update_oper.operator_type_id,
                operator_type = update_oper.operator_type.name,
                status =  update_oper.status,
                )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_oper_by_id(session:AsyncSession, oper_id:int):
    try:
        empl_dal = OperatorDal(session)

        delete_user = await empl_dal.delete_operator_by_type(oper_id=oper_id)

        return {'success':True} if delete_user else {'success':False}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")