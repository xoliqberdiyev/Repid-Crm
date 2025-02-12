# import pytest

# from database import schemas, session
# from sqlalchemy.ext.asyncio import AsyncSession
# from fastapi import Depends
# from dals import user_dal

# @pytest.fixture
# def create_user(db:AsyncSession = Depends(session.get_db_test)):
#     emp_dal = user_dal.EmployeeDal(session=db)
#     emp_dal.create_position('Backend developer')
#     emp_dal.create_employee('Shahzod',"Abdashev",'qiyinkodjuda',1, '+998949252954','2024-01-01','2024-01-01',10000,'shaha_king')

         
# class TestAllGetRequest:
#     def test_list_users(create_user, db:AsyncSession = Depends(session.get_db_test)):
#         emp_dal = user_dal.EmployeeDal(session=db)
#         data = emp_dal.get_all_employee()

#         return schemas.ShowEmployee(data)




