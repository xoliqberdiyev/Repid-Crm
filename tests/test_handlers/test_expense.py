from datetime import date

from tests.conftest import create_test_auth_headers_for_user
from database.models import UserType


class TestExpense:
    async def create_test_user(self,create_user_in_database, create_position_from_database):
        position = await create_position_from_database("Backend")

        user_data = {
            "username": "test",
            "last_name": "test",
            "first_name": "test",
            "phone_number": "+345345345345",
            "salary": 100000,
            "position_id": position,
            "password": "testjkjk",
            "is_active": True,
            "user_type": UserType.admin,
            "date_of_birth": date(2024, 1, 1),
            "date_of_jobstarted": date(2024, 1, 1),
            "created_time": date(2024, 1, 1),
        }
        user_id = await create_user_in_database(**user_data)
        return (user_data,user_id)

    async def test_create_expense(self, client, create_user_in_database, 
                                create_position_from_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        data_project = {
                        'name':'katta pul kerak',
                        'price_paid':'10000',
                        'description':'Hello world',
                        'date_paied':'2024-01-03',
                        'from_whom':'oybek',
                        'type':'for_office',
                        }
        
        resp = client.post('/expence', headers=create_test_auth_headers_for_user(user_data[0]['username']),
                           json = data_project)
        
        assert resp.status_code == 200
        data_json = resp.json()
        assert data_json['name'] == data_project['name']
        assert data_json['price_paid'] == data_project['price_paid']
        assert data_json['description'] == data_project['description']
        assert data_json['from_whom'] == data_project['from_whom']
        assert data_json['date_paied'] == '2024-01-03T00:00:00'
        assert data_json['type'] == data_project['type']
   
    async def test_list_expense(self, client, create_user_in_database,
                                create_position_from_database, create_expense_in_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        data_expense = await create_expense_in_database(
            name='Kitob',
            price_paid='1000',
            description='soqqa katta',
            date_paied=date(2025,1,1),
            from_whom='oybek',
            type='for_office'
        )

        resp = client.get('/expence', headers=create_test_auth_headers_for_user(username=user_data[0]['username']),
                          params={'type':'for_office'})

        assert resp.status_code == 200
        data_json = resp.json()
        assert data_json['items'][0]['name'] == data_expense.name
        assert data_json['items'][0]['price_paid'] == data_expense.price_paid
        assert data_json['items'][0]['description'] == data_expense.description
        assert data_json['items'][0]['date_paied'] == '2025-01-01T00:00:00'
        assert data_json['items'][0]['from_whom'] == 'oybek'
        assert data_json['items'][0]['type'] == 'for_office'
    
    async def test_delete_expense(self,client,create_user_in_database,
                                create_position_from_database, create_expense_in_database):
        user_data = await self.create_test_user(create_user_in_database, create_position_from_database)

        data_expense = await create_expense_in_database(
            name='Kitob',
            price_paid='1000',
            description='soqqa katta',
            date_paied=date(2025,1,1),
            from_whom='oybek',
            type='for_office'
        )

        resp = client.delete('/expence', headers=create_test_auth_headers_for_user(username=user_data[0]['username']),
                             params={'expense_id':data_expense.id})
        assert resp.status_code == 200
        data_json = resp.json()
        assert data_json['success'] == True
        assert data_json['message'] == 'Deleted successfully'


        