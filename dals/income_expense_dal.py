from datetime import datetime, timedelta

from sqlalchemy import select, update, delete, and_, func, case, cast, BigInteger, extract, or_ ,desc, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from database import models, schemas


class IncomeExepnseDal:
    def __init__(self, db_session:AsyncSession):
        self.db_session = db_session

    async def create_income_data(self,body:schemas.CreateIncomeStudent):
        query = models.IncomeData(
            name = body.name,
            real_price = body.real_price,
            pay_price=body.pay_price,
            date_paied=body.date_paid,
            position=body.position,
            type=body.type,
            description=body.description
        )

        self.db_session.add(query)

        await self.db_session.commit()

        return query
    
    async def get_list_income_student(self,start_date,end_date,type):

        query = select(models.IncomeData).where(models.IncomeData.type==type)
        if start_date and end_date:
            query = select(models.IncomeData).where(and_(models.IncomeData.type=='from_student',
                                                         models.IncomeData.date_paied.between(start_date,end_date)))

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def delete_income_student(self, income_student_id:int):
        query = delete(models.IncomeData).where(models.IncomeData.id==income_student_id)

        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False
    
    async def update_income_student(self, income_student_id:int, **kwargs):
        query = update(models.IncomeData).where(models.IncomeData.id==income_student_id).values(**kwargs).returning(models.IncomeData)

        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
    
    async def create_income_project(self,body:schemas.CreateIncomeProject):
        query = models.IncomeData(
            project_id = body.project_id,
            pay_price=body.pay_price,
            type='from_project',
            description=body.description,
            date_paied=body.date_paid
        )


        self.db_session.add(query)

        await self.db_session.commit()

        return query
    
    async def get_list_income_project(self,start_date,end_date):
        query = select(models.IncomeData).where(models.IncomeData.type=='from_project')
        if start_date and end_date:
            query = select(models.IncomeData).where(and_(models.IncomeData.type=='from_project',
                                                         models.IncomeData.date_paied.between(start_date,end_date)))

        res = await self.db_session.execute(query)
        return res.scalars().all()

    async def delete_income_project(self, income_project_id:int):
        query = delete(models.IncomeData).where(and_(models.IncomeData.type=='from_project'),(models.IncomeData.id==income_project_id))

        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False
    
    async def update_income_project(self, body,income_project_id):

        query = (update(models.IncomeData).where(and_(models.IncomeData.type=='from_project'),(models.IncomeData.id==income_project_id))
                 .values(pay_price=body['pay_price'],
                         project_id=body['project_id'],
                         description=body['description'],
                         date_paied=body['date_paid']
                 ).returning(models.IncomeData))

        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
    
    async def get_income_statistics(self,start_date, end_date):
        query = (
                select(
                    func.sum(
                        case(
                            (models.IncomeData.type == "from_student", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_from_student"),
                    func.sum(
                        case(
                            (models.IncomeData.type == "from_project", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_from_project"),
                    func.sum(
                        case(
                            (models.IncomeData.type == "investor", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_investor"),
                    func.sum(cast(models.IncomeData.pay_price, BigInteger)).label("grand_total")
                )
            )
        if start_date and end_date:
            query = (
                select(
                    func.sum(
                        case(
                            (models.IncomeData.type == "from_student", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_from_student"),
                    func.sum(
                        case(
                            (models.IncomeData.type == "from_project", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_from_project"),
                    func.sum(
                        case(
                            (models.IncomeData.type == "investor", cast(models.IncomeData.pay_price, BigInteger)),
                            else_=0,
                        )
                    ).label("total_investor"),
                    func.sum(cast(models.IncomeData.pay_price, BigInteger)).label("grand_total")
                )
            ).where(
                models.IncomeData.date_paied.between(start_date, end_date)
            )

        result = await self.db_session.execute(query)
        stats = result.one()

        return stats
    
    async def create_expene_by_type(self,body:schemas.CreateNewExpence):
        query = models.ExpenseData(
            name=body.name,
            description=body.description,
            price_paid=body.price_paid,
            date_paied=body.date_paied,
            from_whom=body.from_whom,
            real_price=body.real_price,
            type=body.type
        )

        self.db_session.add(query)
        await self.db_session.commit()

        return query
    
    async def get_list_expense(self,status,start_date, end_date, order,from_whom):
        query = (select(models.ExpenseData)
                    .where(and_(models.ExpenseData.type==status, models.ExpenseData.type!='employee_salary'))
                    .order_by(desc(models.ExpenseData.date_paied)))
        
        if order == 'old':
            query = (select(models.ExpenseData)
                    .where(and_(models.ExpenseData.type==status, models.ExpenseData.type!='employee_salary'))
                    .order_by(asc(models.ExpenseData.date_paied)))
        if from_whom:
            query = (select(models.ExpenseData)
                    .where(and_(models.ExpenseData.type==status, models.ExpenseData.type!='employee_salary',
                                models.ExpenseData.from_whom==from_whom))
                    .order_by(desc(models.ExpenseData.date_paied)))
        if start_date and end_date:
            query = select(models.ExpenseData).where(and_(models.ExpenseData.type==status, 
                                                          models.ExpenseData.type!='employee_salary',
                                                          models.ExpenseData.date_paied.between(start_date,end_date)))

        res = await self.db_session.execute(query)

        return res.scalars().all()
    
    async def update_expense_by_type(self, expense_id ,**kwargs):
        query = update(models.ExpenseData).where(models.ExpenseData.id==expense_id).values(kwargs).returning(models.ExpenseData)
        res = await self.db_session.execute(query)

        return res.scalar_one_or_none()
    
    async def delete_expense(self, expense_id):
        query = delete(models.ExpenseData).where(models.ExpenseData.id==expense_id)
        res = await self.db_session.execute(query)

        if res.rowcount > 0:
            return True
        return False

    async def create_expense_employee(self, body:schemas.CreatingExepnseEmployee):
        query = models.ExpenseData(
            employee_salary_id=body.employee_id,
            type='employee_salary',
            price_paid=body.price_paied,
            date_paied=body.date_paid
        )

        self.db_session.add(query)
        await self.db_session.commit()
        return query
    
    async def get_employee_id(self, user_id:int):
        query = select(models.Employees).join(models.Position).where(and_(
                models.Employees.id == user_id,
                models.Employees.is_active == True
            )
        ).options(selectinload(models.Employees.position))
        result = await self.db_session.execute(query)
        employee = result.scalars().first()  
        return employee

    async def update_expense_employee(self, body:schemas.UpdateExpenseSalary,income_employee_id:int):
        query = update(models.ExpenseData).where(models.ExpenseData.id==income_employee_id).values(
            price_paid=body['price_paid'],
            employee_salary_id=body['user_id'],
            date_paied=body['date_paid']
        ).returning(models.ExpenseData)

        result = await self.db_session.execute(query)
        await self.db_session.commit()

        returnigng_query = (select(models.ExpenseData)
                .join(models.Employees)  # Ensure Employees is joined correctly
                .join(models.Position)  # Ensure Position is joined correctly
                .where(
                    and_(
                        models.ExpenseData.type == 'employee_salary',
                        models.ExpenseData.id==income_employee_id
                    )
                )
                .options(
                    selectinload(models.ExpenseData.employee_salary),  # From root entity
                    selectinload(models.ExpenseData.employee_salary).selectinload(models.Employees.position)  # Nested relationship
                ))
        
        await self.db_session.commit()
        result = await self.db_session.execute(returnigng_query)
        return result.scalar_one_or_none()

    async def get_list_expense_employee(self,start_date, end_date,order):
        query = (
                select(models.ExpenseData)
                .join(models.Employees)  # Ensure Employees is joined correctly
                .join(models.Position)  # Ensure Position is joined correctly
                .where(
                    and_(
                        models.ExpenseData.type == 'employee_salary',
                    )
                )
                .options(
                    selectinload(models.ExpenseData.employee_salary),  # From root entity
                    selectinload(models.ExpenseData.employee_salary).selectinload(models.Employees.position)  # Nested relationship
                )
                .order_by(desc(models.ExpenseData.date_paied))
            )
        if order=='old':
            query = (
                select(models.ExpenseData)
                .join(models.Employees)  # Ensure Employees is joined correctly
                .join(models.Position)  # Ensure Position is joined correctly
                .where(
                    and_(
                        models.ExpenseData.type == 'employee_salary',
                        models.Employees.is_active == True,
                    )
                )
                .options(
                    selectinload(models.ExpenseData.employee_salary),  # From root entity
                    selectinload(models.ExpenseData.employee_salary).selectinload(models.Employees.position)  # Nested relationship
                )
                .order_by(asc(models.ExpenseData.date_paied))
            )
        
        if start_date and end_date:
            query = (
                select(models.ExpenseData)
                .join(models.Employees)  # Ensure Employees is joined correctly
                .join(models.Position)  # Ensure Position is joined correctly
                .where(
                    and_(
                        models.ExpenseData.type == 'employee_salary',
                        models.Employees.is_active == True,
                        models.ExpenseData.date_paied.between(start_date, end_date)       
                    )
                )
                .options(
                    selectinload(models.ExpenseData.employee_salary),  # From root entity
                    selectinload(models.ExpenseData.employee_salary).selectinload(models.Employees.position)  # Nested relationship
                )
            )


        result = await self.db_session.execute(query)
        all_user =  result.scalars().all()
        return all_user
        
    async def get_pie_chart_expense(self,start_date, end_date):
        query = (
            select(
                func.sum(
                    case(
                        (models.ExpenseData.type == "employee_salary", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_from_student"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "for_office", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_for_office"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "smm_service", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_smm_service"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "renting", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_renting"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "office_item", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_office_item"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "tax", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_tax"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "other_expense", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_other_expense"),
                func.sum(cast(models.ExpenseData.price_paid, BigInteger)).label("grand_total")
            )
        )
        if start_date and end_date:
            query = (
            select(
                func.sum(
                    case(
                        (models.ExpenseData.type == "employee_salary", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_from_student"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "for_office", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_for_office"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "smm_service", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_smm_service"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "renting", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_renting"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "other_expense", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_other_expense"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "office_item", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_office_item"),
                func.sum(
                    case(
                        (models.ExpenseData.type == "tax", cast(models.ExpenseData.price_paid, BigInteger)),
                        else_=0,
                    )
                ).label("total_tax"),
                func.sum(cast(models.ExpenseData.price_paid, BigInteger)).label("grand_total")
            )
            .where(
                models.ExpenseData.date_paied.between(start_date, end_date)
            )
        )

        result = await self.db_session.execute(query)
        stats = result.one()

        return stats
    
    async def line_graph_month_expense(self,month,year):
        if year == None:
            current_year = datetime.utcnow().year
        elif year:
            current_year = year

        if month == 12:
              month_for = month - 1 
        else:
            month_for = month

        days_in_month = [
            (datetime(current_year, month_for, day).day, 0)  # Default to (day, 0)
            for day in range(1, (datetime(current_year, month_for+1, 1) - timedelta(days=1)).day + 1)
        ]
        days_dict = dict(days_in_month)  

        result = await self.db_session.execute(
            select(
                extract('day', models.ExpenseData.date_paied).label('day'),
                func.sum(cast(models.ExpenseData.price_paid, BigInteger)).label('total_real_price')
            )
            .where(
                and_(
                    extract('year', models.ExpenseData.date_paied) == current_year,  # Filter by current year
                    extract('month', models.ExpenseData.date_paied) == month # Filter by selected month
                )
            )
            .group_by(extract('day', models.ExpenseData.date_paied))
            .order_by(extract('day', models.ExpenseData.date_paied))
        )
        
        # Update dictionary with real values from DB
        for row in result.fetchall():
            days_dict[int(row.day)] = row.total_real_price

        # Convert dictionary back to list sorted by day
        return sorted(days_dict.items())
    
    async def line_graph_month_income(self,month,year):
        if year==None:
            current_year = datetime.utcnow().year
        elif year:
            current_year = year

        if month == 12:
              month_for = month - 1 
        else:
            month_for = month

        days_in_month = [
            (datetime(current_year, month_for, day).day, 0)  # Default to (day, 0)
            for day in range(1, (datetime(current_year, month_for+1, 1) - timedelta(days=1)).day + 1)
        ]
        days_dict = dict(days_in_month)  

        result = await self.db_session.execute(
            select(
                extract('day', models.IncomeData.date_paied).label('day'),
                func.sum(cast(models.IncomeData.pay_price, BigInteger)).label('total_real_price')
            )
            .where(
                and_(
                    extract('year', models.IncomeData.date_paied) == current_year,  # Filter by current year
                    extract('month', models.IncomeData.date_paied) == month,
                )
                
            )
            .group_by(extract('day', models.IncomeData.date_paied))
            .order_by(extract('day', models.IncomeData.date_paied))
        )
        
        for row in result.fetchall():
            days_dict[int(row.day)] = row.total_real_price

        # Convert dictionary back to list sorted by day
        return sorted(days_dict.items())

    async def line_graph_year_income(self,year):
        if year is None:
            year = datetime.utcnow().year

        months_dict = {month: 0 for month in range(1, 13)}

        # Fetch income data for the given year
        result = await self.db_session.execute(
            select(
                extract('month', models.IncomeData.date_paied).label('month'),
                func.sum(cast(models.IncomeData.pay_price, BigInteger)).label('total_real_price')
            )
            .where(
                and_(
                    extract('year', models.IncomeData.date_paied) == year
                )
            )
            .group_by(extract('month', models.IncomeData.date_paied))
            .order_by(extract('month', models.IncomeData.date_paied))
        )

        # Update dictionary with actual values from the database
        for row in result.fetchall():
            months_dict[int(row.month)] = row.total_real_price

        return sorted(months_dict.items())    
    
    async def line_graph_year_expense(self, year=None):
        now = datetime.utcnow()
        current_month = now.month
        current_year = now.year

        if year is None:
            start_date = now.replace(year=current_year - 1, month=current_month, day=1)
            end_date = now
        else:
            start_date = datetime(year, 1, 1)
            end_date = datetime(year, 12, 31)

        print(f"Fetching data from {start_date} to {end_date}")  # Debugging print

        # Create months order: last month → this month last year
        months_order = [(current_month - 1 + i) % 12 + 1 for i in range(13)]

        # Initialize dictionary with zero values
        months_dict = {month: 0 for month in months_order}

        # Fetch data from DB
        result = await self.db_session.execute(
            select(
                extract('month', models.ExpenseData.date_paied).label('month'),
                func.sum(cast(models.ExpenseData.price_paid, BigInteger)).label('total_real_price')
            )
            .where(models.ExpenseData.date_paied.between(start_date, end_date))
            .group_by(extract('month', models.ExpenseData.date_paied))
            .order_by(extract('month', models.ExpenseData.date_paied))
        )

        fetched_data = result.fetchall()
        print("Fetched Data:", fetched_data)  # Debugging print

        # Update dictionary with actual values
        for row in fetched_data:
            print(f"Updating month {int(row.month)} with value {row.total_real_price}")  # Debugging print
            months_dict[int(row.month)] = row.total_real_price

        # Return data in correct order
        sorted_result = [(month, months_dict[month]) for month in months_order]
        print("Final Sorted Result:", sorted_result)  # Debugging print
        return sorted_result

    async def get_only_expense(self, start_date, end_date):
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)  # Get the date 30 days ago

        result = await self.db_session.execute(
            select(func.sum(cast(models.ExpenseData.price_paid, BigInteger))).where(
                models.ExpenseData.date_paied >= thirty_days_ago  # Filter only last 30 days
            )
        )

        if start_date and end_date:
            result = await self.db_session.execute(
            select(func.sum(cast(models.ExpenseData.price_paid, BigInteger))).where(
                models.ExpenseData.date_paied.between(start_date, end_date)  
            )
        )

        total_expense = result.scalar() or 0  # Handle case where no expenses exist

        return total_expense
    
    async def get_only_income(self,start_date, end_date):
        thirty_days_ago = datetime.utcnow() - timedelta(days=30)  # Get the date 30 days ago

        result = await self.db_session.execute(
            select(func.sum(cast(models.IncomeData.pay_price, BigInteger))).where(
        
                models.IncomeData.date_paied >= thirty_days_ago,
                or_(
                        models.IncomeData.project.has(models.Project.is_deleted == False),  # Include valid projects
                        models.IncomeData.project_id.is_(None)  # Include from_student (no project)
                    )
            )
        )
        if start_date and end_date:
            result = await self.db_session.execute(
            select(func.sum(cast(models.IncomeData.pay_price, BigInteger))).where(
        
                models.IncomeData.date_paied.between(start_date, end_date),
                or_(
                        models.IncomeData.project.has(models.Project.is_deleted == False),  # Include valid projects
                        models.IncomeData.project_id.is_(None)  # Include from_student (no project)
                    )
            )
        )

        total_expense = result.scalar() or 0  # Handle case where no expenses exist

        return total_expense
    
    async def get_only_employee_count(self,start_date, end_date):
        result = await self.db_session.execute(
            select(func.count()).where(and_(models.Employees.is_active==True))
        )
        if start_date and end_date:
            result = await self.db_session.execute(
            select(func.count()).where(and_(models.Employees.is_active==True,
                                            models.Employees.created_time.between(start_date, end_date)))
        )

        return result.scalar() or 0 
    
    async def gef_only_project_count(self, start_date, end_date):
        result = await self.db_session.execute(
            select(func.count()).where(models.Project.is_deleted==False)
        )
        if start_date and end_date:
            result = await self.db_session.execute(
            select(func.count()).where(and_(models.Project.is_deleted==False,
                                            models.Project.start_date.between(start_date, end_date)))
        )

        return result.scalar() or 0
    
    async def get_projects_done_chart(self, year):
        if year is None:
            year = datetime.utcnow().year

        months_dict = {month: 0 for month in range(1, 13)}

        resutl = await self.db_session.execute(

            select(
                extract('month', models.Project.start_date).label('month'),
                extract('year', models.Project.start_date),
                func.count().label('count_project')
            )
            .where(
                and_(models.Project.status==models.StatusProject.done, 
                     models.Project.is_deleted==False,
                     extract('year', models.Project.start_date) == year)
                
                )
            .group_by(extract('month', models.Project.start_date),
                    extract('year', models.Project.start_date))
            .order_by(extract('month', models.Project.start_date),
                      extract('year', models.Project.start_date))
        )
        for row in resutl.fetchall():
            months_dict[int(row.month)] = row.count_project
        print(months_dict)

        return months_dict

    async def get_project_done_pie_chart(self):
        result = await self.db_session.execute(
            select(
                func.count(
                    case((models.Project.status == models.StatusProject.done, 1))
                ).label("project_done_count"),
                func.count(
                    case((models.Project.status == models.StatusProject.in_progres, 1))
                ).label("project_progres_count")
            ).where(models.Project.is_deleted == False)
        )

        return result.one_or_none()



