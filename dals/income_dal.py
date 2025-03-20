from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, delete, and_, func, case, cast, BigInteger, extract, or_ 

from database import models, schemas


class IncomeDal:
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
        months_order = [((current_month - 1 + i) % 12 + 1) for i in range(13)]
        print(months_order)
        # Initialize dictionary with zero values
        months_dict = {month: 0 for month in months_order}
        print(months_dict)
        # Fetch data from DB
        result = await self.db_session.execute(
            select(
                extract('month', models.IncomeData.date_paied).label('month'),
                func.sum(cast(models.IncomeData.pay_price, BigInteger)).label('total_real_price')
            )
            .where(models.IncomeData.date_paied.between(start_date, end_date))
            .group_by(extract('month', models.IncomeData.date_paied))
            # .order_by(extract('month', models.IncomeData.date_paied))
        )

        fetched_data = result.fetchall()
        print("Fetched Data:", fetched_data)  # Debugging print

        # Update dictionary with actual values
        for row in fetched_data:
            print(f"Updating month {int(row.month)} with value {row.total_real_price}")  # Debugging print
            months_dict[row.month] = row.total_real_price

        return {month:months_dict[month] for month in months_order}
    
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
    