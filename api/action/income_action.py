from datetime import datetime
from fastapi.exceptions import HTTPException

from dals import income_dal, user_dal
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas


async def _create_income_student(session:AsyncSession, body:schemas.CreateIncomeStudent):
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            income_student = await in_ex_dal.create_income_data(body=body)

            return schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.pay_price,
                description=income_student.description  ,
                left_price=int(income_student.real_price) - int(income_student.pay_price) if income_student.real_price else 0 ,
                date_paied=income_student.date_paied,
                position=income_student.position,
                type=income_student.type
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_list_income_student(session:AsyncSession,start_date,end_date,type):
    if start_date is None and end_date is None:
        pass
    elif start_date and end_date:
        pass
    else:
        raise HTTPException(status_code=422, detail='Bro you need to fill both of them')
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            income_students = await in_ex_dal.get_list_income_student(start_date,end_date,type)

            return [
                schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.pay_price,
                description=income_student.description,
                left_price=int(income_student.real_price) - int(income_student.pay_price) if income_student.real_price else 0,
                date_paied=income_student.date_paied,
                position=income_student.position,
                type=income_student.type
            )
                for income_student in income_students
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_income_student(session:AsyncSession, income_student_id:int):
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            income_student = await in_ex_dal.delete_income_student(income_student_id)

            if income_student:
                return {'success':True,
                        'message':'Muvvafaqiyatli ochirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_income_student(session:AsyncSession, income_student_id:int, body:dict):
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            income_student = await in_ex_dal.update_income_student(income_student_id=income_student_id,
                                                                **body)

            return schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.pay_price,
                description=income_student.description,
                left_price=int(income_student.real_price) - int(income_student.pay_price) if income_student.real_price else 0,
                date_paied=income_student.date_paied,
                position=income_student.position,
                type=income_student.type
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_income_project(session:AsyncSession, body:schemas.CreateIncomeProject):
        try:
            in_ex_dal = income_dal.IncomeDal(session)
            empl_dal = user_dal.EmployeeDal(session)

            income_project = await in_ex_dal.create_income_project(body=body)

            project_with_id = await empl_dal.get_project_id(project_id=body.project_id)

            return schemas.ShowIncomeProject(
                id=income_project.id,
                name=project_with_id.name,
                project_id=project_with_id.id,
                real_price=project_with_id.price,
                date_start=project_with_id.start_date,
                description=income_project.description,
                pay_price=income_project.pay_price,
                date_end=project_with_id.end_date,
                type=income_project.type,
                left_price=int(project_with_id.price) - int(income_project.pay_price),
                date_paied=income_project.date_paied,
                programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await empl_dal.get_programmers_by_project_id(project_with_id.id)],

            )
        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_list_income_project(session: AsyncSession,start_date,end_date):
    if start_date is None and end_date is None:
        pass
    elif start_date and end_date:
        pass
    else:
        raise HTTPException(status_code=422, detail='Bro you need to fill both of them')
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)
            empl_dal = user_dal.EmployeeDal(session)

            income_projects = await in_ex_dal.get_list_income_project(start_date,end_date)

            result = []
            for income_project in income_projects:
                project_with_id = await empl_dal.get_project_id(project_id=income_project.project_id)
                if project_with_id:
                    programmers = await empl_dal.get_programmers_by_project_id(project_with_id.id)

                    result.append(
                        schemas.ShowIncomeProject(
                            id=income_project.id,
                            name=project_with_id.name,
                            project_id=project_with_id.id,
                            real_price=project_with_id.price,
                            date_start=project_with_id.start_date,
                            description=income_project.description,
                            pay_price=income_project.pay_price,
                            date_end=project_with_id.end_date,
                            type=income_project.type,
                            left_price=int(project_with_id.price) - int(income_project.pay_price),
                            date_paied=income_project.date_paied,
                            programmers=[
                                schemas.ProgrammerSchema.model_validate(programmer) for programmer in programmers
                            ],
                        )
                    )

            return result
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_income_project(session:AsyncSession, income_project_id:int):
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            income_project = await in_ex_dal.delete_income_project(income_project_id=income_project_id)

            if income_project:
                return {'success':True,
                        'message':'Muvvafaqiyatli ochirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_income_project(session:AsyncSession, body:dict,income_project_id:int):
    try:
        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)
            empl_dal = user_dal.EmployeeDal(session)

            income_project = await in_ex_dal.update_income_project(body,income_project_id)

            project_with_id = await empl_dal.get_project_id(project_id=income_project.project_id)

            return schemas.ShowIncomeProject(
                id=income_project.id,
                name=project_with_id.name,
                real_price=project_with_id.price,
                date_start=project_with_id.start_date,
                project_id=project_with_id.id,
                pay_price=income_project.pay_price,
                date_end=project_with_id.end_date,
                description=income_project.description,
                type=income_project.type,
                left_price=int(project_with_id.price) - int(income_project.pay_price),
                date_paied=income_project.date_paied,
                programmers=[schemas.ProgrammerSchema.model_validate(programmer) for programmer in await empl_dal.get_programmers_by_project_id(project_with_id.id)],

            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_income_piechart(session:AsyncSession, start_date, end_date):
    if start_date and end_date or (start_date is None  and end_date is None):
        pass
    else:
        raise HTTPException(status_code=422, detail='Bro you need to fill both of them')
    try:
        in_ex_dal = income_dal.IncomeDal(session)

        total = await in_ex_dal.get_income_statistics(start_date, end_date)

        return {
            'total_income_student':total.total_from_student,
            'total_income_project':total.total_from_project,
            'total_investor':total.total_investor,
            'total':total.grand_total,
            'percentage_income_student':(total.total_from_student/total.grand_total)*100,
            'percentage_income_project':(total.total_from_project/total.grand_total)*100,
            'percentage_income_investor':(total.total_investor/total.grand_total)*100
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")


async def _get_line_graph_month_income(month:int, session:AsyncSession,year:int):
    try:
        if month == None or year==None:
            month = datetime.utcnow().month

        if month > 12:
            raise HTTPException(status_code=403, detail='Date time sholud be in range 1..12')

        async with session.begin():
            in_ex_dal = income_dal.IncomeDal(session)

            line_graph = await in_ex_dal.line_graph_month_income(month=month,year=year)

            monthly_data = {
                day: total_real_price
                for day, total_real_price in line_graph
            }

            return monthly_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_line_graph_year_income(year:int,session:AsyncSession):
    async with session.begin():
        in_ex_dal = income_dal.IncomeDal(session)

        line_graph = await in_ex_dal.line_graph_year_income(year=year)
        
        return line_graph
