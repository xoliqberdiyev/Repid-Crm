import asyncio

from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, delete, or_, func, cast, BigInteger
from sqlalchemy.orm import joinedload

from database import models, schemas


class CommonDal:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def get_income_expected_val(self):
        query = select(models.ExcpectedValue).where(models.ExcpectedValue.type == models.StatusExpectedVAlue.income)
        res = await self.db_session.execute(query)

        if res is not None:
            return res.scalars().all()
        print(res)
    
    async def get_expence_expected_val(self):
        query = select(models.ExcpectedValue).where(models.ExcpectedValue.type == models.StatusExpectedVAlue.expense)
        res = await self.db_session.execute(query)

        if res is not None:
            return res.scalars().all()
        
    async def create_expected_val(self,body:schemas.CreateExpectedValue):
        res = models.ExcpectedValue(
            name=body.name,
            date=body.date,
            description=body.description,
            type=body.type,
            price=body.price
        )

        self.db_session.add(res)

        await self.db_session.flush()
        return res
        
    async def delete_expected_val(self, expected_val_id:int):
        query = delete(models.ExcpectedValue).where(models.ExcpectedValue.id == expected_val_id)

        res = await self.db_session.execute(query)

        await self.db_session.commit() 

        if res.rowcount > 0:
            return True
        return False
        
    async def update_expected_val(self, expected_avl_id:int, **kwargs):
        query = update(models.ExcpectedValue).where(models.ExcpectedValue.id == expected_avl_id).values(kwargs)

        res = await self.db_session.execute(query)
        await self.db_session.commit()

        if res.rowcount > 0:
            return True
        return False
    
    async def get_programmers_by_task_id(self,task_id):
        result = await self.db_session.execute(
            select(models.Employees).join(models.TaskProgrammer).where(and_(models.TaskProgrammer.task_id == task_id),(models.Employees.is_active==True))
        )
        return result.scalars().all()
    
    async def create_new_task(self, body:schemas.CreateNewTask,image_task:str):
        new_task = models.Task(
            name=body.name,
            image_task=image_task,
            start_date=body.start_date,
            end_date=body.end_date,
            description=body.description,
            status=body.status
        )
        self.db_session.add(new_task)
        await self.db_session.flush() 

        task_programmers = [
            models.TaskProgrammer(
                task_id=new_task.id,
                programmer_id=int(programmer_id)
            )
            for programmer_id in body.programmer_ids
        ]
        self.db_session.add_all(task_programmers)

        await self.db_session.commit()

        return new_task
    
    async def get_all_tasks(self, status:str, task_id:int):
        query = select(models.Task).where(models.Task.is_deleted==False)
        if status:
            query = select(models.Task).where(and_(models.Task.is_deleted==False),(models.Task.status==status))
        elif task_id:
            query = select(models.Task).where(and_(models.Task.is_deleted==False),(models.Task.id==task_id))
        elif status and task_id:
            query = select(models.Task).where(and_(models.Task.is_deleted==False),(models.Task.id==task_id),(models.Task.status==status))
        
        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def delete_new_task(self, task_id:int):
        query = update(models.Task).where(models.Task.id==task_id).values(is_deleted=True)

        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False

    async def update_status_task(self,status:str, task_id:int):
        query = update(models.Task).where(models.Task.id==task_id).values(status=status).returning(models.Task)

        res = await self.db_session.execute(query)
        return res.scalar_one_or_none()
    
    async def update_new_task(self, task_id: int, body: schemas.UpdateNewTask,image_task:str):
        task_query = (
            update(models.Task)
            .where(models.Task.id == task_id)
            .values(
                name=body.name,
                start_date=body.start_date,
                end_date=body.end_date,
                description=body.description,
                image_task=image_task
            )
            .returning(models.Task)
        )
        task_result = await self.db_session.execute(task_query)
        updated_task = task_result.scalar_one_or_none()

        if not updated_task:
            return None

        await self.db_session.execute(
            delete(models.TaskProgrammer).where(models.TaskProgrammer.task_id == task_id)
        )

        for programmer_id in body.programmer_ids:
            task_programmer = models.TaskProgrammer(
                task_id=task_id,
                programmer_id=programmer_id,
            )
            self.db_session.add(task_programmer)

        await self.db_session.commit()

        return updated_task

    async def get_list_oper_type(self):
        query = select(models.OperatorType)

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def create_operator_type(self, name):
        query = models.OperatorType(
            name=name
        )

        self.db_session.add(query)
        await self.db_session.commit()

        return query
    
    async def search_query(self, query_):
        query, query2 = await asyncio.gather(
            self.db_session.execute(
                select(models.Employees)
                .where(
                    models.Employees.is_active == True,
                    or_(
                        models.Employees.first_name.contains(query_),
                        models.Employees.username.contains(query_),
                        models.Employees.last_name.contains(query_),
                    )
                )
            ),
            self.db_session.execute(
                select(models.Project)
                .where(models.Project.is_deleted==False,
                ).filter(models.Project.name.contains(query_))
            )
        )

        employees = query.scalars().all()
        projects = query2.scalars().all()

        return employees, projects
    
    async def create_login_password(self, login:str, password:str, name:str):
            result = models.LoginPasswordNote(
                name=name,
                login=login,
                password=password
            )   
            self.db_session.add(result)

            await self.db_session.commit()

            return result
    
    async def update_login_password(self,login_note_id, **kwargs):
        result = await self.db_session.execute(
            update(models.LoginPasswordNote)
            .where(models.LoginPasswordNote.id==login_note_id)
            .values(kwargs).returning(models.LoginPasswordNote)
        )

        await self.db_session.commit()

        return result.scalar_one_or_none()
    
    async def delete_login_password(self, note_id:int):
        result = await self.db_session.execute(
            delete(models.LoginPasswordNote).where(models.LoginPasswordNote.id==note_id)
        )

        await self.db_session.commit()

        if result.rowcount > 0:
            return True
        return False

    async def get_all_login_password_note(self):
        result = await self.db_session.execute(
            select(models.LoginPasswordNote)
        )
        return result.scalars().all()
    
    async def get_cash_income(self):
        result_income = await self.db_session.execute(
            select(
                func.sum(cast(models.IncomeData.pay_price,BigInteger)
                )))
        result_expense = await self.db_session.execute(
            select(
                func.sum(cast(models.ExpenseData.price_paid,BigInteger)
                )))
        


        return (result_income.scalar_one(),result_expense.scalar_one())
    
   