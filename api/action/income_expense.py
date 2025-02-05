from datetime import datetime

from fastapi.exceptions import HTTPException

from dals import income_expense_dal,  user_dal

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from database import schemas, models


async def _create_income_student(session:AsyncSession, body:schemas.CreateIncomeStudent):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            income_student = await in_ex_dal.create_income_data(body=body)

            return schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.pay_price,
                left_price=int(income_student.real_price) - int(income_student.pay_price),
                date_paied=income_student.date_paied,
                position=income_student.position,
                type=income_student.type
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _get_list_income_student(session:AsyncSession,start_date,end_date):
    if start_date is None and end_date is None:
        pass
    elif start_date and end_date:
        pass
    else:
        raise HTTPException(status_code=422, detail='Bro you need to fill both of them')
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            income_students = await in_ex_dal.get_list_income_student(start_date,end_date)

            return [
                schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.pay_price,
                left_price=int(income_student.real_price) - int(income_student.pay_price),
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
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            income_student = await in_ex_dal.delete_income_student(income_student_id)

            if income_student:
                return {'success':True,
                        'message':'Muvvafaqiyatli ochirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
        
async def _update_income_student(session:AsyncSession, income_student_id:int, body:dict):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            income_student = await in_ex_dal.update_income_student(income_student_id=income_student_id,
                                                                **body)
            
            return schemas.ShowIncomeStudent(
                id=income_student.id,
                name=income_student.name,
                real_price=income_student.real_price,
                pay_price=income_student.real_price,
                left_price=int(income_student.real_price) - int(income_student.real_price),
                date_paied=income_student.date_paied,
                position=income_student.position,
                type=income_student.type
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
# ------------------------------------------------------------------------------------------------------------------
from fastapi_pagination.utils import disable_installed_extensions_check
async def _create_income_project(session:AsyncSession, body:schemas.CreateIncomeProject):
        try:
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
            empl_dal = user_dal.EmployeeDal(session)

            income_project = await in_ex_dal.create_income_project(body=body)

            project_with_id = await empl_dal.get_project_id(project_id=body.project_id)

            return schemas.ShowIncomeProject(
                id=income_project.id,
                name=project_with_id.name,
                project_id=project_with_id.id,
                real_price=project_with_id.price,
                date_start=project_with_id.start_date,
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
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
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
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            income_project = await in_ex_dal.delete_income_project(income_project_id=income_project_id)

            if income_project:
                return {'success':True,
                        'message':'Muvvafaqiyatli ochirildi'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
        
async def _update_income_project(session:AsyncSession, body:dict,income_project_id:int):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
            empl_dal = user_dal.EmployeeDal(session)

            income_project = await in_ex_dal.update_income_project(body,income_project_id)

            project_with_id = await empl_dal.get_project_id(project_id=income_project.project_id)

            return schemas.ShowIncomeProject(
                id=income_project.id,
                name=project_with_id.name,
                real_price=project_with_id.price,
                date_start=project_with_id.start_date,
                pay_price=income_project.pay_price,
                date_end=project_with_id.end_date,
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
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        total = await in_ex_dal.get_income_statistics(start_date, end_date)

        return {
            'total_income_student':total.total_from_student,
            'total_income_project':total.total_from_project,
            'total':total.grand_total,
            'percentage_income_student':(total.total_from_student/total.grand_total)*100,
            'percentage_income_project':(total.total_from_project/total.grand_total)*100,
        }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_expence_type(session:AsyncSession,
                               body:schemas.CreateNewExpence):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            create_expense = await in_ex_dal.create_expene_by_type(body=body)

            return schemas.ShowExpenseType(
                id=create_expense.id,
                name=create_expense.name,
                price_paid=create_expense.price_paid,
                description=create_expense.description,
                date_paied=create_expense.date_paied,
                real_price=create_expense.real_price,
                remainder_price=int(create_expense.real_price) - int(create_expense.price_paid) if create_expense.real_price!=None else None,
                type=create_expense.type
            )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _update_expense_by_type(session:AsyncSession, expense_id:int ,body:dict):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            update_expese = await in_ex_dal.update_expense_by_type(expense_id=expense_id, **body)
            return schemas.ShowExpenseType(
                id=update_expese.id,
                name=update_expese.name,
                price_paid=update_expese.price_paid,
                description=update_expese.description,
                date_paied=update_expese.date_paied,
                real_price=update_expese.real_price,
                remainder_price=int(update_expese.real_price) - int(update_expese.price_paid) if update_expese.real_price!=None else None,
                type=update_expese.type
            )

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _get_expence_type_list(session:AsyncSession,status:str,start_date,end_date):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            expense_list = await in_ex_dal.get_list_expense(status=status,start_date=start_date,end_date=end_date)

            
            return [
                    schemas.ShowExpenseType(
                        id=expense_.id,
                        name=expense_.name,
                        price_paid=expense_.price_paid,
                        description=expense_.description,
                        date_paied=expense_.date_paied,
                        real_price=expense_.real_price,
                        remainder_price=int(expense_.real_price) - int(expense_.price_paid) if expense_.real_price!=None else None,
                        type=expense_.type
                    )
                    for expense_ in expense_list
                ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _delete_expense(expense_id:int, session:AsyncSession):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            delete_expense = await in_ex_dal.delete_expense(expense_id=expense_id)

            if delete_expense:
                return {'success':True,
                        'message':"Deleted successfully"}
            return {'success':False,
                        'message':"Error occured"}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _create_expense_employee(body:schemas.CreatingExepnseEmployee, session:AsyncSession):
    try:
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
        get_employee = await in_ex_dal.get_employee_id(user_id = body.employee_id)

        if not get_employee:
            return {"success": False, "message": "Employee not found or inactive."}

        create_expense = await in_ex_dal.create_expense_employee(body=body)

        if not create_expense:
            return {"success": False, "message": "Error happend"}
        
        return schemas.ShowExpenseEmployee(
            id=create_expense.id,
            pay_paied=create_expense.price_paid,
            type=create_expense.type,
            user_id = get_employee.id,
            date_last_paied=create_expense.date_paied,
            remainder_price=int(get_employee.salary) - int(create_expense.price_paid),
            first_name=get_employee.first_name,
            last_name=get_employee.last_name,
            position_name=get_employee.position.name,
            start_of_job=get_employee.date_of_jobstarted,
            salary=get_employee.salary,
            img=f'uploads/{get_employee.image}',
            phone_number=get_employee.phone_number,
        )
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")
    
async def _update_expense_employee(body:dict,session:AsyncSession,income_employee_id:int):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            update_expense_employee = await in_ex_dal.update_expense_employee(body,income_employee_id)
            if update_expense_employee:
                return {'success':True,
                        'message':'Successfully updated'}
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")

async def _list_expense_employee(session: AsyncSession,start_date, end_date):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            list_expense_employee = await in_ex_dal.get_list_expense_employee(start_date, end_date)

            return [
                schemas.ShowExpenseEmployee(
                    id=expense_employee.id,
                    pay_paied=expense_employee.price_paid,
                    type=expense_employee.type,
                    user_id=expense_employee.employee_salary.id,
                    date_last_paied=expense_employee.date_paied,
                    remainder_price=int(expense_employee.employee_salary.salary) - int(expense_employee.price_paid),
                    first_name=expense_employee.employee_salary.first_name,
                    last_name=expense_employee.employee_salary.last_name,
                    position_name=expense_employee.employee_salary.position.name,
                    start_of_job=expense_employee.employee_salary.date_of_jobstarted,
                    salary=expense_employee.employee_salary.salary,
                    img=f'uploads/{expense_employee.employee_salary.image}',
                    phone_number=expense_employee.employee_salary.phone_number,
                )
                for expense_employee in list_expense_employee
            ]
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")    
    
async def _expense_pie_chart(session:AsyncSession, start_date, end_date):
    if start_date and end_date or (start_date is None  and end_date is None):
        pass
    else:
        raise HTTPException(status_code=422, detail='Bro you need to fill both of them')
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            pie_chart_expesne = await in_ex_dal.get_pie_chart_expense(start_date, end_date)
            return {
                'salary':pie_chart_expesne.total_from_student,
                'office':pie_chart_expesne.total_for_office,
                'smm':pie_chart_expesne.total_smm_service,
                'renting':pie_chart_expesne.total_renting,
                'other':pie_chart_expesne.total_other_expense,
                'total_expenses':pie_chart_expesne.grand_total

            }

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")    

async def _get_line_graph_month_expense(month:int, session:AsyncSession,year:int):
    try:
        if month == None or year == None:
            month = datetime.utcnow().month

        if month > 12:
            raise HTTPException(status_code=403, detail='Date time sholud be in range 1..12')
        
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

            line_graph = await in_ex_dal.line_graph_month_expense(month=month, year=year)

            monthly_data = {
                day: total_real_price
                for day, total_real_price in line_graph
            }

            return monthly_data
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")    
    
async def _get_line_graph_month_income(month:int, session:AsyncSession,year:int):
    try:
        if month == None or year==None:
            month = datetime.utcnow().month

        if month > 12:
            raise HTTPException(status_code=403, detail='Date time sholud be in range 1..12')
        
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

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
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        line_graph = await in_ex_dal.line_graph_year_income(year=year)

        monthly_data = {
            month: total_real_price
            for month, total_real_price in line_graph
        }

        return monthly_data
    
async def _get_line_graph_year_expense(year:int, session:AsyncSession):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        line_graph = await in_ex_dal.line_graph_year_expense(year=year)

        yearly_data = {
            month: total_real_price
            for month, total_real_price in line_graph
        }
        return yearly_data
    
async def _get_main_dashboard(session:AsyncSession, start_date, end_date):
    async with session.begin():
        in_ex_dal = income_expense_dal.IncomeExepnseDal(session)

        only_income = await in_ex_dal.get_only_income(start_date, end_date)
        only_expense = await in_ex_dal.get_only_expense(start_date, end_date)
        only_employee = await in_ex_dal.get_only_employee_count(start_date, end_date)
        only_project = await in_ex_dal.gef_only_project_count(start_date, end_date)

        return {
            'last_month_income': only_income,
            'last_month_expense': only_expense,
            'employee_count':only_employee,
            'project_count':only_project
        }
    
async def _get_projects_done_chart(session:AsyncSession, year:int):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
            projects_done_chart = await in_ex_dal.get_projects_done_chart(year=year)

            return {
                month:count_project
                for month, count_project in projects_done_chart.items()
            }


    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")    
    
async def _get_project_done_pie_chart(session:AsyncSession):
    try:
        async with session.begin():
            in_ex_dal = income_expense_dal.IncomeExepnseDal(session)
            project_done_pie_chart = await in_ex_dal.get_project_done_pie_chart()
            print(project_done_pie_chart)

            return {
                'count_done_project':project_done_pie_chart.project_done_count,
                'count_progres_project':project_done_pie_chart.project_progres_count,
                'total_project':project_done_pie_chart.project_done_count+project_done_pie_chart.project_progres_count
            }
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch income values: {str(e)}")    


 


