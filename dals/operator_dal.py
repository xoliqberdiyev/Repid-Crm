from datetime import datetime
from fastapi import HTTPException

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, delete, or_
from sqlalchemy.orm import joinedload, selectinload

from database import models, schemas
from utils.hashing import Hasher



class OperatorDal:
    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def create_operator(self,full_name:str, 
                              phone_number:str, 
                              description:str,operator_type_id:int):
        query = models.Operator(
            full_name=full_name,
            phone_number=phone_number,
            description=description,
            operator_type_id=operator_type_id,
        )

        self.db_session.add(query)
        await self.db_session.flush()  # Commit the session to persist the data
        # await self.db_session.refresh(query)  # Refresh to access relationships
        return query
    
    async def get_operator_type_by_id(self,op_id:int):
        query = (
            select(models.OperatorType)
            .where(models.OperatorType.id == op_id)
        )
        result = await self.db_session.execute(query)
        operator_with_type = result.scalar_one()
        return operator_with_type.name
    
    async def get_all_operator(self, oper_type_id:int,status:str, search:str):
        query = select(models.Operator).join(models.OperatorType).options(joinedload(models.Operator.operator_type))

        if oper_type_id and status:
            query = select(models.Operator).where(and_(models.Operator.operator_type_id == oper_type_id, models.Operator.status == status)).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        elif oper_type_id:
            query = select(models.Operator).where(models.Operator.operator_type_id == oper_type_id).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        elif status:
            query = select(models.Operator).where(models.Operator.status == status).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        elif search:
            query = select(models.Operator).where(or_(models.Operator.full_name.ilike(f"%{search}%"), models.Operator.phone_number.ilike(f"%{search}%"))).join(models.OperatorType).options(joinedload(models.Operator.operator_type))

        res = await self.db_session.execute(query.order_by(models.Operator.id))

        return res.scalars().all()
    
    async def update_operator_by_type(self, oper_id, **kwargs):
        query = update(models.Operator).where(models.Operator.id==oper_id).values(kwargs).returning(models.Operator)
        res = await self.db_session.execute(query)
        await self.db_session.commit()

        res_oper = res.scalar_one_or_none()

        res_query = select(models.Operator).where(and_(models.Operator.id==res_oper.id)).join(models.OperatorType).options(joinedload(models.Operator.operator_type))
        res_ = await self.db_session.execute(res_query)

        return res_.scalar_one_or_none()

    async def delete_operator_by_type(self,oper_id):
        query = delete(models.Operator).where(models.Operator.id==oper_id)

        res = await self.db_session.execute(query)
        await self.db_session.commit()
        return True if res.rowcount >0 else False

    async def change_operator_status(self,oper_id:int, status:str):
        if status not in models.StatusOperator.__members__.values():
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.values())}")
        
        try:
            status_enum = models.StatusOperator[status]  # Convert string to StatusOperator enum
        except KeyError:
            raise ValueError(f"Invalid status: {status}. Must be one of {list(models.StatusOperator.__members__.keys())}")

        query = (
            update(models.Operator)
            .values(status=status_enum)
            .filter_by(id = oper_id)
            .returning(models.Operator) 
        )

        res = await self.db_session.execute(query) 
  
        return res.scalar_one_or_none()


    